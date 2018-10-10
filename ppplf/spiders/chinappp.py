# -*- coding: utf-8 -*-
import re

import scrapy

from ppp.items import PppItem


class ChinapppSpider(scrapy.Spider):
    name = 'chinappp'
    # allowed_domains = ['http://www.chinappp.cn/projectcenter/finance.html']
    start_urls = ['http://www.chinappp.cn/projectcenter/projectinfo_local_1_1.html','http://www.chinappp.cn/projectcenter/projectinfo_fgw_1_1.html']
    item=PppItem()
    def parse(self, response):
        quotes=response.css('.library_one')
        namelist=quotes.css('h3 a::text').extract()
        urllist=quotes.css('.step_right').css('a::attr("href")').extract()
        for eachurl, eachname in zip(urllist, namelist):
            eachurl='http://www.chinappp.cn/projectcenter/'+eachurl
            yield scrapy.Request(eachurl,meta={"name":eachname},callback=self.parsedetail)
        nexturl='http://www.chinappp.cn'+ response.css('.pagination').css('a::attr("href")').extract()[-2]
        yield scrapy.Request(url=nexturl, callback=self.parse)
    def parsedetail(self,response):
        ChinapppSpider.item['name']=response.meta['name']
        table=response.css('.table_content').css('tr td').extract()
        pattern=re.compile(r'<td.*?>(.*?)</td>')
        overview=[]
        for i in table:
            i=i.replace('\t','').replace(' ','').replace('\n','').replace('\r','')
            if len(pattern.findall(i)) > 0:
                overview.append(pattern.findall(i)[0])
            else:
                overview.append('')
        print(overview)
        ChinapppSpider.item['investment']=overview[1]
        ChinapppSpider.item['operationmode']=overview[3]
        ChinapppSpider.item['area']=overview[5]
        ChinapppSpider.item['mechanism']=overview[7]
        ChinapppSpider.item['industry']=overview[9]
        ChinapppSpider.item['level']=overview[11]
        ChinapppSpider.item['time']=overview[13]
        ChinapppSpider.item['term']=overview[15]
        ChinapppSpider.item['tele']=overview[19]
        ChinapppSpider.item['people']=overview[21]
        ChinapppSpider.item['schedule']= response.css('.active dd::text').extract()[0]
        tableview=response.css('.table_content_czb').css('tr td').css('td').extract()
        if len(tableview)>0:
            interview=[]
            for i in tableview:
                i = i.replace('\t', '').replace(' ', '').replace('\n', '').replace('\r', '')
                if len(pattern.findall(i)) > 0:
                    interview.append(pattern.findall(i)[0])
                else:
                    interview.append('')
            ChinapppSpider.item['overview']=interview[1]
            ChinapppSpider.item['scope']=interview[3]
        else:
            if len(response.css('.main_content').css('p::text').extract())>0:
                ChinapppSpider.item['overview']=response.css('.main_content').css('p::text').extract()[0].replace('\t', '').replace(' ', '').replace('\n','').replace('\r', '')
            else:
                ChinapppSpider.item['overview']=''
            ChinapppSpider.item['scope']=''
        yield ChinapppSpider.item
