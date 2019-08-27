# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from myapp.items import MyappItem

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['zuowen.com']
    start_urls = [
        #春天作文的列表
        # 'http://www.zuowen.com/redianhuti/chuntian/ctll',
        'http://www.zuowen.com/redianhuti/chuntian/mldct',
        # 'http://www.zuowen.com/redianhuti/chuntian/xzct',
        # 'http://www.zuowen.com/redianhuti/chuntian/ctdgs',
        # 'http://www.zuowen.com/redianhuti/chuntian/ctdxy',
        # 'http://www.zuowen.com/redianhuti/chuntian/wact',
        # 'http://www.zuowen.com/redianhuti/chuntian/chunfeng',
        # 'http://www.zuowen.com/redianhuti/chuntian/chunyu',
        # 'http://www.zuowen.com/redianhuti/chunyouzw/chunyou',
        #夏天作文的列表
        # 'http://www.zuowen.com/redianhuti/xiatianzw/'
        #秋天作文的列表
        # 'http://www.zuowen.com/redianhuti/qiutianzw/qiutian/'
        # 'http://www.zuowen.com/redianhuti/qiutianzw/qiutiangyzw/'
        # 'http://www.zuowen.com/redianhuti/qiutianzw/qiutiantyzw/'
        # 'http://www.zuowen.com/redianhuti/qiutianzw/qiutianthzw/'
        # 'http://www.zuowen.com/redianhuti/qiutianzw/qiutiansyzw/'
        # 'http://www.zuowen.com/redianhuti/qiutianzw/qiutianxyzw/'
        #冬天作文的列表
        # 'http://www.zuowen.com/redianhuti/dongtianzw/dongtian/'
    ]

    def parse(self, response):
        firstpage = response.xpath("//div[@class='artlist_l_t']/h1/a/@href").extract()
        print(firstpage)
        lastpage = response.xpath("//div[@class='artpage']/a/text()").extract()
        print(response.request.url)


        #构造下一页的请求地址
        for i in range(1, int(lastpage[-2])+1):
        # for i in range(3, 4):
            if i==1:
                yield Request(firstpage[0], callback=self.parse_list)
            else:
                nexturl = response.request.url + "index_" + str(i) + ".shtml"
                print(nexturl)
                yield Request(nexturl, callback = self.parse_list)

    #提取每页的文章链接并访问
    def parse_list(self, response):
        currentpagelist = response.xpath("//div[@class='artbox_l_t']/a/@href").extract()
        for i in range(0, len(currentpagelist)):
            yield Request(currentpagelist[i], callback = self.parse_article)

    #提取文章内容页页面的信息
    def parse_article(self, response):
        item = MyappItem()
        #获取标题
        item["articletitle"] = response.xpath("normalize-space(//h1[@class='h_title']/text())").extract()
        #获取文章每段的内容
        rawdetail = response.xpath("//div[@class='con_content']/p/text()").extract()
        item["articledetail"] = []
        #清除每段内容前的\r\n\t
        for i in rawdetail:
            item["articledetail"].append(i.replace('\r', '').replace('\n', '').replace('\t', ''))
        item["articleurl"] = response.request.url
        print(item["articleurl"])
        return item
