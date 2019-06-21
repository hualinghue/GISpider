import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from lxml import etree
from core import GetImgAddress
from urllib.parse import urljoin
import json

class WeiYiSpider(GetImgAddress.BaseSpider):
    name  = "唯一桌面"
    model = 'static_get'
    display = True
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
    display = True
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
            url = tree.xpath('//div[@class="pic"]/p/a/img/@src')
            if not url:
                print(url)
                raise ValueError
            img_size = self.storage(url=url[0],label=5)
class QibaSpider(GetImgAddress.BaseSpider):
    # json获取数据
    def __init__(self):
        self.name  = "87g"
        self.model = 'json_get'
        self.exclude_urls = []
        self.start_urls = []
        self.link = r''  #分页正则
        self.init_url()
    display = False
    def init_url(self,):
        # 批量生成请求连接
        for i in range(1,9):
            self.start_urls.append('http://www.87g.com/index.php?m=content&c=content_ajax&a=picture_page&siteid=1&catid=34&page=%d&_=1560741069911'%i)
    def parse_item(self, response):    #解析数据函数
        response_text = response.text.encode('utf8')[3:].decode('utf8')
        json_dic = json.loads(response_text)
        print(json_dic)
class TPSpider(GetImgAddress.BaseSpider):
    name  = "7160图片大全"
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
            self.name = name
            self.model = 'static_get'
            self.start_urls = url
            self.exclude_urls = []
            self.link = r'\d+_\d+.html'  # 分页正则
        def parse_item(self, response):
            tree = etree.HTML(response.text)
            url = tree.xpath('//div[@class="picsbox picsboxcenter"]//img/@src')[0]
            tp_id = self.storage(url=url,label=6)


#
# aa = TPSpider()
# bb = GetImgAddress.DriveEngine(aa)
# bb.run()
