# -*- coding: utf-8 -*-
import re

import scrapy_redis
import requests
import scrapy

from MavenScrapy.items import MavenscrapyItem

class MavenSpider(scrapy.Spider):
    name = 'maven'
    # allowed_domains = ['http://central.maven.org/maven2/'] #允许爬取多个页面
    start_urls = ['http://central.maven.org/maven2/']
    item = MavenscrapyItem()

    def parse(self, response):
        quote=response.css('#contents').css('a::attr("href")').extract() #解析maven的初始网站
        urllist=[]
        for i in quote:
            if '../' not in i and '.xml' not in i and '.txt' not in i: #判断是否为文件夹
                    urllist.append(self.start_urls[0]+i)
                    yield scrapy.Request(url=self.start_urls[0]+i, callback=self.parsedetail,meta={"url":self.start_urls[0]+i}) #如果是文件夹就用parsedetail进行解析
    #判断是否为版本
    def isversion(self,versionurl):
        isversion=False
        html=requests.get(versionurl).text
        pattern=re.compile(r'.*title=\"(.*?)\".*')
        result=re.findall(pattern,html)
        for i in result:
            if 'pom' in i or 'jar' in i : #观察得到版本里面的内容包含pom或者jar
                isversion=True
                return isversion
        return isversion

    def parsedetail(self,response):
        isproject=False
        quote=response.css('#contents').css('a::attr("href")').extract()
        detailurl=response.meta['url']
        if len(quote)>0 and '.xml' in quote[-1]: #如果最后一个有xml，那么此处页面就包含版本
            isproject = True
        if isproject:
            groupid=''
            artifactid=''
            for i in quote:
                #从xml里面提取出groupid和artifactid
                if '.xml' in i and '.md5' not in i and '.sha1' not in i:
                    xmlstring=requests.get(detailurl+i).text
                    pattern = re.compile(r'.*<groupId>(.*?)</groupId>\s*.*<artifactId>(.*?)</artifactId>.*')
                    result = re.findall(pattern,xmlstring)
                    if result is not None :
                        print(result)
                        print(result[0])
                        groupid=result[0][0]
                        artifactid=result[0][1]
                    else:
                        groupid = ''
                        artifactid = ''
            for i in quote:
                version_url=detailurl+i
                if '../' not in i and '.xml' not in i and '.txt' not in i:
                    if self.isversion(version_url)==True: #当前文件夹是版本
                        yield scrapy.Request(url=version_url,callback=self.parseversiondetail,meta={"version":i.replace('/',''),"version_url":version_url,"groupid":groupid,"artifactid":artifactid})
                    elif self.isversion(version_url)==False: #当前文件夹不是版本
                        yield scrapy.Request(url=version_url,callback=self.parsedetail,meta={"url":version_url})
        else: #此处界面不包含版本，全都是一般的文件夹
            for i in quote:
                if '../' not in i:
                    yield scrapy.Request(url=detailurl+i,callback=self.parsedetail,meta={"url":detailurl+i})

    #解析版本
    def parseversiondetail(self,response):
        MavenSpider.item['version']=response.meta['version']
        MavenSpider.item['version_url']=response.meta['version_url']
        MavenSpider.item['groupid']=response.meta['groupid']
        MavenSpider.item['artifactid']=response.meta['artifactid']
        quote = response.css('#contents').css('a::attr("href")').extract()
        #版本里面是否含有pom，source，jar下载地址，以及md5和sha1
        ispomdl=False
        issourcesdl=False
        isjarmd5=False
        isjarsha1=False
        isjardl=False

        for i in quote:
            if 'doc' not in i and 'dependencies' not in i: #排除掉包含doc和dependencies的
                if 'sources' not in i and '.jar.md5' in i : #获取jar_md5
                    isjarmd5=True
                    MavenSpider.item['jar_md5']=requests.get(response.meta['version_url']+i).text
                elif 'sources' not in i and '.jar.sha1' in i:#获取jar_sha1，一下几个同理
                    isjarsha1=True
                    MavenSpider.item['jar_sha1'] =requests.get(response.meta['version_url']+i).text
                elif 'sources' not in i and '.jar' in i and '.md5' not in i and '.asc' not in i and '.sha1' not in i:
                    isjardl=True
                    MavenSpider.item['jar_download_url']=response.meta['version_url'] + i
                elif 'pom' in i and '.md5' not in i and '.asc' not in i and '.sha1' not in i:
                    ispomdl=True
                    MavenSpider.item['pom_download_url']=response.meta['version_url'] + i
                elif 'sources' in i and '.md5' not in i and '.asc' not in i and '.sha1' not in i:
                    issourcesdl=True
                    MavenSpider.item['jar_source_download_url']=response.meta['version_url'] + i
        #判断以上几个变量是否存在版本中，不存在就赋默认值
        if isjarmd5 == False:
            MavenSpider.item['jar_md5'] = ''
        if isjarsha1 == False:
            MavenSpider.item['jar_sha1'] = ''
        if isjardl == False:
            MavenSpider.item['jar_download_url'] = ''
        if ispomdl==False:
            MavenSpider.item['pom_download_url']=''
        if issourcesdl==False:
            MavenSpider.item['jar_source_download_url'] =''
        yield MavenSpider.item