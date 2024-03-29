import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from lxml import etree
from core import GetImgAddress
from urllib.parse import urljoin
from conf import Setting

class WeiYiSpider(GetImgAddress.BaseSpider):
    name  = "唯一桌面"
    model = 'static_get'
    display = False
    start_urls = ['http://www.mmonly.cc/mmtp/']
    exclude_urls = []
    link = r'list_9_\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        tree = etree.HTML(response.text)
        a_list = tree.xpath('//div[@id="infinite_scroll"]/div')
        for a in a_list:
            url = a.xpath('.//div[@class="ABox"]/a/@href')
            next_obj =self.NextBianSpider(url)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,):
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            a_list = tree.xpath('//div[@id="big-pic"]')
            for a in a_list:
                url = a.xpath('.//img/@src')[0]
                img_size=self.storage(url=url,label=5)
class BianSpider(GetImgAddress.BaseSpider):
    name  = "彼岸桌面"
    display = False
    model = 'static_get'
    start_urls = ['http://www.netbian.com/meinv/']
    exclude_urls = []
    link = r'/meinv/index_\d+.htm'  #分页正则
    def parse_item(self,response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath('//div[@class="list"]/ul/li/a')
        for a in a_list:
            url = a.xpath('./@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r''  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url = tree.xpath('//div[@class="pic"]//img/@src')
            if not url:
                print(url,self.start_urls)
                raise ValueError
            img_size = self.storage(url=url[0],label=5)
class TPSpider(GetImgAddress.BaseSpider):
    name  = "TP"
    model = 'static_get'
    display = False
    start_urls = ['https://www.7160.com/xiaohua/']
    exclude_urls = []
    link = r'list_6_\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//div[@class='news_bom-left']//li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            file_name = self.text_analysis(a.xpath('./a/@title')[0])
            next_obj =self.NextBianSpider([urljoin(response.url,url)],"%s/%s"%(self.name,file_name))
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name+"_"
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url = tree.xpath('//div[@class="picsbox picsboxcenter"]//img/@src')[0]
            tp_id = self.storage(url=url,label=6)
class MTSSpider(GetImgAddress.BaseSpider):
    name  = "XG"
    model = 'static_get'
    display = True
    start_urls = ['https://www.meitulu.com/t/xinggan/']
    exclude_urls = []
    link = r'https://www.meitulu.com/t/xinggan/\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//ul[@class='img']/li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name+"_"
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'/item/\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url_list = tree.xpath('//div[@class="content"]/center/img/@src')
            headers = Setting.HEADERS
            headers['Referer'] = 'https://www.meitulu.com/img.html'
            for url in url_list:
                tp_id = self.storage(url=url,label=3,headers=headers)
class MTKApider(GetImgAddress.BaseSpider):
    name  = "KA"
    model = 'static_get'
    display = True
    start_urls = ['https://www.meitulu.com/t/keai/']
    exclude_urls = []
    link = r'https://www.meitulu.com/t/keai/\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//ul[@class='img']/li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name+"_"
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'/item/\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url_list = tree.xpath('//div[@class="content"]/center/img/@src')
            headers = Setting.HEADERS
            headers['Referer'] = 'https://www.meitulu.com/img.html'
            for url in url_list:
                print("下载",url)
                tp_id = self.storage(url=url,label=1,headers=headers)
class MTQSpider(GetImgAddress.BaseSpider):
    name  = "QC"
    model = 'static_get'
    display = True
    start_urls = ['https://www.meitulu.com/t/qingchun/']
    exclude_urls = []
    link = r'https://www.meitulu.com/t/qingchun/\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//ul[@class='img']/li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name+"_"
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'/item/\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url_list = tree.xpath('//div[@class="content"]/center/img/@src')
            headers = Setting.HEADERS
            headers['Referer'] = 'https://www.meitulu.com/img.html'
            for url in url_list:
                tp_id = self.storage(url=url,label=2,headers=headers)
class MTLLpider(GetImgAddress.BaseSpider):
    "美图录_萝莉"
    name  = "LL"
    model = 'static_get'
    display = True
    start_urls = ['https://www.meitulu.com/t/loli/']
    exclude_urls = []
    link = r'https://www.meitulu.com/t/loli/\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//div[@class='boxs']/ul/li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name+"_"
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'/item/\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url_list = tree.xpath('//div[@class="content"]/center/img/@src')
            headers = Setting.HEADERS
            headers['Referer'] = 'https://www.meitulu.com/img.html'
            for url in url_list:
                tp_id = self.storage(url=url,label=5,headers=headers)
class MTBLpider(GetImgAddress.BaseSpider):
    "美图录_爆乳"
    name  = 'BL'
    model = 'static_get'
    display = True
    start_urls = ['https://www.meitulu.com/t/baoru/']
    link = r'https://www.meitulu.com/t/baoru/\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//div[@class='boxs']/ul/li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name+"_"
            self.model = 'static_get'
            self.start_urls = url
            self.link = r'/item/\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url_list = tree.xpath('//div[@class="content"]/center/img/@src')
            headers = Setting.HEADERS
            headers['Referer'] = 'https://www.meitulu.com/img.html'
            for url in url_list:
                tp_id = self.storage(url=url,label=7,headers=headers)
class MTNSpider(GetImgAddress.BaseSpider):
    "美图录_女神"
    name  = "NS"
    model = 'static_get'
    display = True
    start_urls = ['https://www.meitulu.com/t/nvshen/']
    exclude_urls = []
    link = r'https://www.meitulu.com/t/nvshen/\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//div[@class='boxs']/ul/li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'/item/\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url_list = tree.xpath('//div[@class="content"]/center/img/@src')
            headers = Setting.HEADERS
            headers['Referer'] = 'https://www.meitulu.com/img.html'
            for url in url_list:
                tp_id = self.storage(url=url,label=4,headers=headers)
class MTQTpider(GetImgAddress.BaseSpider):
    "美图录_翘臀"
    name  = "QT"
    model = 'static_get'
    display = True
    start_urls = ['https://www.meitulu.com/t/youhuo/']
    exclude_urls = []
    link = r'https://www.meitulu.com/t/\w+/\d+.html'  #分页正则
    def parse_item(self, response):    #解析数据函数
        print(response.url)
        tree = etree.HTML(response.text)
        a_list = tree.xpath("//div[@class='boxs']/ul/li")
        for a in a_list:
            url = a.xpath('./a/@href')[0]
            next_obj =self.NextBianSpider([urljoin(response.url,url)],self.name)
            GetImgAddress.DriveEngine(next_obj).run()
    class NextBianSpider(GetImgAddress.BaseSpider):   #处理详情页
        def __init__(self,url,name):
            self.name = name
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'/item/\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url_list = tree.xpath('//div[@class="content"]/center/img/@src')
            headers = Setting.HEADERS
            headers['Referer'] = 'https://www.meitulu.com/img.html'
            for url in url_list:
                tp_id = self.storage(url=url,label=8,headers=headers)


# aa = MTBLpider()
# bb = GetImgAddress.DriveEngine(aa)
# bb.run()
