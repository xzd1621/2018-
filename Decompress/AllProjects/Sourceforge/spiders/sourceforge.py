# -*- coding: utf-8 -*-
import scrapy
import re
from Sourceforge.items import SourceforgeItem
class SourceforgeSpider(scrapy.Spider):
    name = 'sourceforge'
    # allowed_domains = ['sourceforge.net/directory/?page=1/']#允许爬取多个页面
    start_urls = ['https://sourceforge.net/directory/?page=1/']
    item = SourceforgeItem()
    # 正则匹配得到每一页的url列表
    def sourgehref(hreflist):
        dealhreflist=[]
        pattern=re.compile(r'.*href=\"(.*?)\".*')
        for i in hreflist:
            result=pattern.findall(i)
            dealhreflist.append('https://sourceforge.net'+result[0])
        return dealhreflist

    def parsedetail(self,response):#解析项目详细信息界面
        SourceforgeSpider.item['url']=response.meta['url'] #项目详细页面的url
        SourceforgeSpider.item['name']=response.meta['name'] #项目的名字
        SourceforgeSpider.item['filesurl']=response.meta['filesurl'] #项目下载链接
        SourceforgeSpider.item['introduce_brief']=response.css('.title').css('.summary').css('h3::text').extract_first() #项目简略介绍
        SourceforgeSpider.item['introduce_detail']=response.css('.description::text').extract_first() #项目详细介绍
        SourceforgeSpider.item['downloads']=int(response.css('.stats').css('a::text').extract()[1].replace(',','').replace(' This Week','')) #这个星期的下载数量，可能随时会变化
        SourceforgeSpider.item['last_update_time']=response.css('.stats').css('time::text').extract_first() #最近更新时间
        #项目的star数量
        if response.css('.average::text').extract_first() is None:
            SourceforgeSpider.item['star']=0.0
        else:
            SourceforgeSpider.item['star']=float(response.css('.average::text').extract_first())#the star of item
        temp=response.css('.project-info')
        #判断项目语言，项目编程语言，项目license,项目category是否找得到
        # 找不到就将其赋值为默认的空值
        isfindlan=False #whether the item has language
        isfindcodelan=False #whether the item has the code language
        isfindlic=False #whether the item has licnese
        isfindcat=False #whether the item has the category
        for i in temp:
            if i.css('h4::text').extract_first()=='Languages':
                SourceforgeSpider.item['language']=i.css('a::text').extract()
                isfindlan=True
            elif i.css('h4::text').extract_first()=='Programming Language':
                SourceforgeSpider.item['codelanguage']=i.css('a::text').extract()
                isfindcodelan=True
            elif i.css('h3::text').extract_first()=='License':
                SourceforgeSpider.item['license']=i.css('a::text').extract()
                isfindlic=True
        categorytemp=response.css('.medium-5')
        for i in categorytemp:
            if i.css('h3::text').extract_first()=='Categories':
                SourceforgeSpider.item['category']=i.css('a::text').extract()
                isfindcat=True
                break

        if(isfindlan==False):
            SourceforgeSpider.item['language'] = []
        if(isfindcodelan==False):
            SourceforgeSpider.item['codelanguage'] = []
        if(isfindlic==False):
            SourceforgeSpider.item['license'] = []
        if(isfindcat==False):
            SourceforgeSpider.item['category'] = []
        yield SourceforgeSpider.item

    def parse(self, response):
        quotes=response.css('.projects') #解析每一页
        for quote in quotes:
            urllist=SourceforgeSpider.sourgehref(quote.css('li').css('.result-heading-texts').css('a').extract()) #得到每一页的url列表
            namelist=quote.css('li').css('h2::text').extract() #得到每一页的名字列表
        for eachurl,eachname in zip(urllist,namelist):
                filesurl=eachurl.replace('?source=directory','')+'files'#得到文件下载链接
                yield scrapy.Request(eachurl,meta={"url":eachurl,"filesurl":filesurl,"name":eachname},callback=self.parsedetail)#通过第一页的链接跳转到项目详细信息界面
        next=response.css('.pagination-next a::attr("href")').extract_first() #解析下一页
        url=response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)