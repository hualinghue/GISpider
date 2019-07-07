from urllib.parse import urljoin
import re,time
import random
from selenium import webdriver
from conf import Setting
from selenium.webdriver.chrome.options import Options
import requests
from PIL import Image
import pymongo
import hashlib

class DriveEngine(object):
    def __init__(self,spider_obj):
        self.headers = Setting.HEADERS
        self.spider_obj = spider_obj
        self.func = getattr(self,self.spider_obj.model+'_model')
        self.url_list = set()
        self.old_url = set(spider_obj.exclude_urls)
    def run(self):
        for url in self.spider_obj.start_urls: #循环前台连接
            self.abyss(url)
    def abyss(self,url):
        "重复获取下一页url和html源码进行处理"
        print(url)
        self.old_url.add(url)  #已执行的url
        response_obj = self.func(url)   #获取源码
        response_obj.url = url
        self.spider_obj.parse_item(response_obj)     #调用解析函数
        self.get_page_url(response_obj.text,url)     #调用url提取器
        #判断url集合中是否还有未执行的url
        if self.url_list - self.old_url:
            self.abyss(random.sample(self.url_list - self.old_url, 1)[0])  # 在集合中随机取一个url返回
    def get_page_url(self,response_text,url):
        "获取页面url"
        if self.spider_obj.link:
            response_url_set = self.url_extract(response_text, url)    #获取页面的url
            self.url_list = self.url_list | response_url_set      #合并到url集合
    def url_extract(self,response_text,url):
        "提取页面中的指定规则url"
        re_list = re.findall(self.spider_obj.link,response_text,re.S)
        re_set ={urljoin(url,re_url) for re_url in re_list}
        return re_set
    def static_get_model(self,url):
        'get获取页面html源码'
        response = requests.get(url=url, headers=self.headers,allow_redirects=False)
        print(response)
        # response.encoding = 'utf-8'   #中文乱码
        return response
    def json_get_model(self, url):
        return self.static_get_model(url)
    def dynamic_get_model(self,url):
        '使用selenium模块获取动态html源码'
        #设置无头浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        bro = webdriver.Chrome(executable_path=r'../conf/chromedriver.exe',chrome_options=chrome_options)
        bro.get(url)
        time.sleep(1)
        bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')   #执行js代码
        return bro.page_source
    def dynamic_post_model(self,url):
        pass

class BaseSpider(object):
    def storage(self,url,label,headers=None):
        '下载并保存与本地和mongo'
        self.mongo_obj = self.conne_mongo()
        print("mongo")
        table_obj = self.mongo_obj['tp_image']
        try:
            down = requests.get(url,headers=headers)
        except Exception as e:
            print(url)
            down = requests.get(url, headers=headers)
        print(down)
        if down.status_code ==200:
            down = down.content
            md5_str = self.md5_encryption(down)
            img_path = Setting.SAVE_PATH + md5_str + '.jpg'
            if not table_obj.find_one({'md5':md5_str}): #去重
                self.deposit_loclo(path=img_path,data=down)  #存入本地
                data = {
                    'ctime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'type' : label,
                    'status':1,
                    'md5':md5_str,
                    'size':Image.open(img_path).size   #图片尺寸
                }
                print(url, '下载完成')
                return self.deposit_mongo(data)  #存入mongo
        return None
    def text_analysis(self,text):
        try:  # 处理中文乱码
            text = text.encode('iso-8859-1').decode('gbk')
        except UnicodeEncodeError as e:
            pass
        return text
    def conne_mongo(self):
        client = pymongo.MongoClient(host=Setting.DB_HOST, port=27017)
        db = client[Setting.DB_NAME]
        try:
            db.authenticate(Setting.DB_USER_NAME, Setting.DB_PASSWORD)
            return db
        except Exception as e:
            print('连接mongo失败', e)
    def md5_encryption(self,down):
        hl = hashlib.md5()
        hl.update(down)
        return hl.hexdigest()
    def deposit_mongo(self,data):
        table_obj =  self.mongo_obj['tp_image']
        return table_obj.insert(data)
    def deposit_loclo(self,path,data):
        with open(path, 'wb') as fp:
            fp.write(data)

