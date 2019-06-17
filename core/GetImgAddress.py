from urllib.parse import urljoin
import re,time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os,requests

#! ? , . : ; ” ‘ ` * + - = / \ | _ $ @ # % & ^ ~ {}[]()<>< >
#1 2 3 4 5 6 7 8 9 10

class DriveEngine(object):
    def __init__(self,spider_obj):
        self.headers = {
            'Connection': 'close',  # 当请求成功后,马上断开该次请求(及时释放请求池中的资源)
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.spider_obj = spider_obj
        self.func = getattr(self,self.spider_obj.model+'_model')
        self.url_list = set()
        self.old_url = set(spider_obj.exclude_urls)
    def run(self):
        for url in self.spider_obj.start_urls:
            self.abyss(url)
    def abyss(self,url):
        "重复获取下一页url和html源码进行处理"
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
        response = requests.get(url=url, headers=self.headers)
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
    def storage(self,url,file_name,path):
        '下载并保存与本地'
        down = requests.get(url).content
        file_path = '../file/%s'%path
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        img_path = file_path +'/'+ file_name+'.jpg'
        with open(img_path,'wb') as fp :
            fp.write(down)
        print(img_path, '下载完成')
    def text_analysis(self,text):
        try:  # 处理中文乱码
            text = text.encode('iso-8859-1').decode('gbk')
        except UnicodeEncodeError as e:
            pass
        return text
#
# class Base(object):
#     def __init__(self,data):
#         self.headers = {
#                 "Cookie":"_uab_collina=156059127049657956755503; BAIDU_SSP_lcr=https://www.baidu.com/link?url=VqUYblKfgUn4slbMuXIMuQClQU9liqQmrNMq_VzKdAkUJ8x9r3Hp0c34LI9wfsWb&wd=&eqid=e68a55d10001493e000000065d04ba2e; md=hao123picmeinv; sid=c5wXVelKJeb6G4GKtKxgrtrqHez.HZvoceEoxVoXHw8E0SjXs8FyHBt5zmGkLEOvMDirmnI; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAAC3UlEQVRYR%2BWVvWtUQRTFfzfamCABiSI2FlYhjYovIhb7tAiIohYhRRrRmMVGUiSg%2F4CgECTBQtmoYBMk2CiKEFB3iSBmJZ0oBkUNdkFiE%2FGDHbmzM8vkZT%2FytUZwqvfum5l3z7nn3CsYYwAa5%2BcZ6e0lk06TS6U0ZJcRuQI8FsiVgkt4MNACDAN9ArNLOFJ1y9DXIZtnpSX%2FHRDgNfAQeK8sO7Z3AcccS%2FptP%2FAyiGlF9NwlYBTodXtHgG7gE3AEOADcArqAfmC7xgXe%2BAosuyLdo%2Fq%2FRStWaRlQzaVdQo1eOsBxPSFw28BllWIAPAPcBTT5J44ITfKigTOJc7EjoXTfioFU84iBVuA8MKC2Cj1giu%2BeaU1IK1HyiCPBArDeKwK%2BAPSEBDjCSgD%2FKhCgDbjjZHIqqEgSiErxhfuu%2B%2FR9QSXXA0gEaEdTj2iFbGdLSMsCAeaBQeCa84NP3jIfSC%2BzKiC%2B9Xp%2FxNks%2BSiy7TjwTE%2FwQzWqmkkZVfNPANcDZ3kTbwOyLh76zMf8ESVEZabnrjpJ6jd7Rh%2BWbPbKDVpktTNgLc7XDYjJ5qeAPS7JBxJHJ0zuVQcFM4bQDNhYCMI8mxxEpB%2FDNxqkS1L7xpMgK%2B0JgWz5sYmTH9qYbp5lYsdHe0VpIK6kIg7MTJiwyU32YaRL4ujgAhBFkBkaJA2F1uXuCYF0T%2B9m6%2Fcmplq%2BrBGQIsOHJY72%2BqQto8rQoXZtAKVlsvn7Nq6Vez7Zxm%2B5h5gbkmrXhmBXtT1JaSmYmaa5NQJSJiGTzY8jMpiUja2eMU89wOS7A1JxT12BLGJR5WPMgMRRxyLt%2F%2FNAip44x0bTyS9Ol5NVLbYDaa1jRQJ5YeRoOVnV0v%2B6e2ShwaUT4V05WVkgYdcqFDqSTaLWnrp7JEhgDMzNZLeqNUeKXU7O%2BrlSbo5o7OeGQv%2BjnW%2F5vHkO3371bt%2BCVzVHKs6eOnyo22SvQ65Vr6wF5A8JEnU3FTJQBgAAAABJRU5ErkJggg%3D%3D%2CWin32.1920.1080.24; __auc=61a4fdac16b59c9fbc972c1dbaf; UM_distinctid=16b59ca02ebc6a-078d4610d7d3a8-e353165-1fa400-16b59ca02eca8b; __gads=ID=be6d04136411c8e1:T=1560579547:S=ALNI_MYBwRH5Lhe4TDwRlFBcUbNSdDSeHA; md_href=https%3A%2F%2Fhuaban.com%2Fpins%2F569563890%2F%3Fmd%3Dhao123picmeinv; referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DVqUYblKfgUn4slbMuXIMuQClQU9liqQmrNMq_VzKdAkUJ8x9r3Hp0c34LI9wfsWb%26wd%3D%26eqid%3De68a55d10001493e000000065d04ba2e; __asc=5c994d7916b5a7d034407f3a42c; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543=1560579538,1560591271; CNZZDATA1256903590=356461427-1560577204-%7C1560593404; _cnzz_CV1256903590=md%7Chao123picmeinv%7C1560595225424%26is-logon%7Clogged-out%7C1560595224423; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1560595224",
#                 'Connection':'close', #当请求成功后,马上断开该次请求(及时释放请求池中的资源)
#                 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
#             }
#         self.data = data
#     def get_html(self,url):
#         '获取页面html源码'
#         response = requests.get(url=url,headers=self.headers)
#         # response.encoding = 'utf-8'   #中文乱码
#         return response
#     def post_html(self,url,data):
#         '获取页面html源码'
#         response = requests.post(url=url,data=data)
#         # response.encoding = 'utf-8'   #中文乱码
#         return response
#     def download(self,dl_dic):
#         '下载'
#         file_path = '../file/%s'%self.data['name']
#         if not os.path.exists(file_path):
#             os.mkdir(file_path)
#         dl_dic['m_img_url'] = urljoin(self.data['url'],dl_dic['m_img_url'])
#         img_path = file_path +'/'+ dl_dic['m_img_name']+'.jpg'
#         with open(img_path,'wb') as fp :
#             fp.write(requests.get(dl_dic['m_img_url']).content)
#         # urllib.request.urlretrieve(url=dl_dic['m_img_url'], filename=img_path)
#         print(img_path, '下载完成')
#     def get_new_html(self,re_dic):
#         new_url = urljoin(self.data['url'], re_dic['m_img_url'])
#         new_page_html = self.get_html(new_url).text
#         new_tag_list = self.get_etree_obj(new_page_html, self.data['xpath']['s_img_url'])
#         for new_tag in new_tag_list:
#             re_dic['m_img_url'] = urljoin(self.data['url'], new_tag)
#         return re_dic
#     def get_etree_obj(self, html_text, Statement):
#         '获取etree表达式对象'
#         tree = etree.HTML(html_text)
#         return tree.xpath(Statement)
#
# class Static_Handle(Base):
#     def handle_text(self):
#         '处理'
#         html_text = self.get_html(self.data['url']).text
#         tag_list = self.get_etree_obj(html_text,self.data['xpath']['main'])
#         for tag in tag_list:   #遍历所有标签
#             re_dic = {}
#             for k,v in self.data['xpath']['need_data'].items():  #遍历标签中的内容
#                 re = tag.xpath(v)[0]
#                 try:
#                     re_dic[k] = re.encode('iso-8859-1').decode('gbk')
#                 except UnicodeEncodeError as e:
#                     re_dic[k] = re
#             if self.data["Subpage"]:  #判断是否需要进入子页面获取img
#                 re_dic = self.get_new_html(re_dic)
#             self.download(re_dic)
#         print('over  .')
#
# class Dynamic_Handle(Base):
#     def handle_text(self):
#         '处理'
#
#         model = self.data["model"]
#         func = getattr(self,"%s_html"%model)
#         if model =="post":
#             html_text = func(url=self.data['url'],data=self.data["p_data"])
#         else:
#             html_text = func(url=self.data['url'])
#         if html_text.text.startswith(u'\ufeff'):    # 解决json抱错问题
#             html_text = json.loads(html_text.text.encode('utf8')[3:].decode('utf8'))
#         else:
#             html_text = html_text.json()
#         for k,v in html_text.items():
#             re_dic ={}
#             for ks,vs in  self.data['keys'].items():
#                 re_dic[ks] = v[vs]
#             if self.data['Subpage'] :
#                 re_dic = self.get_new_html(re_dic)
#             self.download(re_dic)



# text = Static_Handle(Setting.rep_addr[1])
# text.handle_text()