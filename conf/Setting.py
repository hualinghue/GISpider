rep_addr = [
    {
        "name":"彼岸桌面",
        "data_type":"Static_Handle",    # Dynamic_Handle动态 或 Static 静态
        "Subpage":True,   # 是否获取子页面图片
        "url":"http://www.netbian.com/meinv/",   #访问路径
        "xpath":{
            "main":'//div[@class="list"]/ul/li/a', # 指定xpath标签的表达式
            's_img_url':'//div[@class="endpage"]/div[@class="pic"]/p/a/img/@src',# 指定xpath子标签表达式
            'need_data':{
                "m_img_url":'./@href',   # 获取url的标签表达式
                "m_img_name":'./b/text()',# 获取name的标签表达式
            },
        }
    },
    {
        "name":"唯一图库",
        "data_type":"Static_Handle",    # Dynamic_Handle动态 或 Static 静态
        "Subpage":True,   # 是否获取子页面图片
        "url":"http://www.mmonly.cc/mmtp/",   #访问路径
        "xpath":{
            "main":"//div[@id='infinite_scroll']/div//div[@class='ABox']/a", # 指定xpath标签的表达式
            's_img_url':'//*[@id="big-pic"]/p/a/img/@src',# 指定xpath子标签表达式
            'need_data':{
                "m_img_url":'./@href',   # 获取url的标签表达式
                "m_img_name":'./img/@alt',# 获取name的标签表达式
            },
        }
    },
    {
        "name":"美女图片",
        "data_type":"Static_Handle",    # Dynamic_Handle动态 或 Static 静态
        "Subpage":True,   # 是否获取子页面图片
        "url":"https://www.zbjuran.com/mei/xinggan/list_13_1.html",   #访问路径
        "xpath":{
            "main":"//div[@class='main']//li", # 指定xpath标签的表达式
            's_img_url':'//*[@class="picbox"]/img/@src',# 指定xpath子标签表达式
            'need_data':{
                "m_img_url":'./div[@class="name"]/a/@href',   # 获取url的标签表达式
                "m_img_name":'./div[@class="name"]/a/@title',# 获取name的标签表达式
            },
        }
    },
    {
        "name": "7160图片大全",
        "data_type": "Static_Handle",  # Dynamic_Handle动态 或 Static 静态
        "Subpage": False,  # 是否获取子页面图片
        "url": "https://www.7160.com/xiaohua/",  # 访问路径
        "xpath": {
            "main": "///div[@class='news_bom-left']//li",  # 指定xpath标签的表达式
            'need_data': {
                "m_img_url": './/img/@src',  # 获取url的标签表达式
                "m_img_name": './/span//text()',  # 获取name的标签表达式
            },
        }
    },
]

