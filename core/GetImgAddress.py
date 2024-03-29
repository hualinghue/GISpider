from urllib.parse import urljoin
from redis import Redis
import random
from selenium import webdriver
from conf import Setting
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pymongo,hashlib,requests,re,time,threading

class DriveEngine(object):
    def __init__(self,spider_obj):
        self.headers = Setting.HEADERS
        self.spider_obj = spider_obj
        self.func = getattr(self,self.spider_obj.model+'_model')
        self.redis = Redis(host='127.0.0.1',port='6379',decode_responses=True)
        self.run()
    def run(self):
        threading_list = []
        #使用多线程
        num = 1
        for url in self.spider_obj.start_urls: #循环前台连接
            self.page_old_url = self.spider_obj.name+ str(num) + 'page_old_url'    #设置redis的集合key名
            self.page_url = self.spider_obj.name + str(num) + 'page_url'
            self.abyss(url)
        #     threading_list.append(threading.Thread(target=self.abyss,args=(url,)))
        #     num +=1
        # for threading_obj in threading_list:
        #     threading_obj.start()
        # for threading_job in threading_list:
        #     threading_job.join()
    def abyss(self,url):
        "重复获取下一页url和html源码进行处理"
        print(url)
        self.redis.sadd(self.page_old_url,url)  #已执行的url
        response_obj = self.func(url)   #获取源码
        self.spider_obj.parse_item(response_obj)     #调用解析函数
        self.get_page_url(response_obj.text,url)     #调用url提取器
        #判断url集合中是否还有未执行的url
        set_nu = self.redis.sdiffstore(self.page_url,self.page_url,self.page_old_url)
        if set_nu:
            # 在redis集合中随机取一个url返回
            next_url = random.sample(self.redis.smembers(self.page_url), 1)[0]
            self.redis.srem(self.page_old_url, next_url)
            self.abyss(next_url)
        else:
            self.redis.delete(self.page_url)
    def get_page_url(self,response_text,url):
        "获取页面url"
        if self.spider_obj.link:
            re_list = re.findall(self.spider_obj.link, response_text, re.S)  #获取页面的url
            for re_url in re_list:
                self.redis.sadd(self.page_url,urljoin(url, re_url) )    #添加到redis中
    def static_get_model(self,url):
        'get获取页面html源码'
        response = requests.get(url=url, headers=self.headers,allow_redirects=False)
        # response.encoding = 'utf-8'   #中文乱码
        return response
    def json_get_model(self, url):
        return self.static_get_model(url)
    def selenium_get_model(self,url):
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
            img_path = Setting.IMG_PATH + md5_str + '.jpg'
            img_ls_path = Setting.IMG_LS_PATH + md5_str + '.jpg'
            if not table_obj.find_one({'md5':md5_str}): #去重
                self.deposit_loclo(path=img_path,data=down)  #存入本地
                img_obj = Image.open(img_path)
                img_ls_size = (200,int(img_obj.size[1]/(img_obj.size[0]/220)))
                data = {
                    'ctime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'type' : label,
                    'status':1,
                    'md5':md5_str,
                    'size':img_obj.size   #图片尺寸
                }
                print(url, '下载完成')
                img_obj.thumbnail(img_ls_size,Image.ANTIALIAS)
                img_obj.save(img_ls_path)
                return self.deposit_mongo(data)  #存入mongo
        return None
    def text_analysis(self,text):
        try:  # 处理中文乱码
            text = text.encode('iso-8859-1').decode('gbk')
        except UnicodeEncodeError as e:
            pass
        return text
    def conne_mongo(self):
        '''连接mongo'''
        client = pymongo.MongoClient(host=Setting.DB_HOST, port=27017)
        db = client[Setting.DB_NAME]
        try:
            db.authenticate(Setting.DB_USER_NAME, Setting.DB_PASSWORD)
            return db
        except Exception as e:
            print('连接mongo失败', e)
    def md5_encryption(self,down):
        '''md5加密'''
        hl = hashlib.md5()
        hl.update(down)
        return hl.hexdigest()
    def deposit_mongo(self,data):
        '''存入mongo'''
        table_obj =  self.mongo_obj[Setting.TABLE_NAME]
        return table_obj.insert(data)
    def deposit_loclo(self,path,data):
        '''存入本地'''
        with open(path, 'wb') as fp:
            fp.write(data)

