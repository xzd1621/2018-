# -*- coding: utf-8 -*-
import os
import urllib

import requests
import scrapy
import re
from loongnix.items import LoongnixItem
from pyquery import PyQuery as pq
from urllib import request


class LongnixSpider(scrapy.Spider):
    name = 'longnix'
    # allowed_domains = ['http://www.loongnix.org/cgit']
    start_urls = ['http://www.loongnix.org/cgit/']

    def parse(self, response):
        namelist=response.css('.sublevel-repo a::text').extract()#获取初始页面的名字列表
        descriptionlist=response.css('.sublevel-repo + td  a::text').extract()#获取初始页面的描述列表
        urllist=[]
        for index, i in enumerate(namelist):
            prourl='http://www.loongnix.org/cgit/'+i+'/'
            urllist.append('http://www.loongnix.org/cgit/'+i+'/')
            yield scrapy.Request(url=prourl+'refs/',meta={'projecturl':prourl,'name':i,'description':descriptionlist[index]},callback=self.parsedetail)#处理每个项目的详细信息页面

    def parsedetail(self,response):
        item=LoongnixItem()
        urlhead='http://www.loongnix.org'
        os.chdir('/home/xu/document/longnixfile/')  # 选择环境默认的文件位置
        item['project_url']=response.meta['projecturl']
        item['project_name']=response.meta['name']
        item['project_description']=response.meta['description']
        tr_result=response.css('.content').css('tr').extract()#解析网站content的每一行
        project_branch=[]
        for tr in tr_result:
            project_dict = {}
            pattern = re.compile(r'<td.*?>(.*?)<\/td>')#正则匹配得到网站的每一列
            tds=re.findall(pattern,tr)
            if len(tds)!=4:#排除没有４列的行，如空行等
                continue
            if len(tds)==4:
                project_dict['name'] = pq(tds[0])('a').html()#得到name
                project_dict['author'] = tds[2]#得到author
                project_dict['age'] = pq(tds[3])('span').html()#得到age
                if ('tar' in tds[1] or 'zip' in tds[1])==False:#如果是branch
                    # tempurl=urlhead+pq(tds[1])('a').attr('href')
                    # html=requests.get(tempurl).text
                    # # html=request.urlopen(tempurl).read().decode('utf-8')
                    # print('**********')
                    #
                    # pattern = re.compile(r'.*<a href=\'(.*?zip)')
                    # result=re.findall(pattern,html)
                    #观察网站的结构，可以拼接出zip的下载链接，而不用点击到下一页再解析
                    dlurl=self.start_urls[0]+response.meta['name']+'/snapshot/'+response.meta['name']+'-'+project_dict['name']+'.zip'
                    project_dict['urllist']=[dlurl]
                    # project_dict['urllist']=[urlhead+i for i in result]
                if ('tar' in tds[1] or 'zip' in tds[1])==True:#如果是tag
                    html=tds[1]
                    print('###########')
                    pattern = re.compile(r'<a href=\"(.*?zip)')#正则匹配得到zip的下载地址
                    result = re.findall(pattern, html)
                    for i in result:
                        print(i)
                    project_dict['urllist'] = [urlhead + i for i in result]#拼接得到zip下载地址列表
                #拼接得到文件的存储路径
                file_path=response.meta['name']+'/'+project_dict['name']+'/'
                for downloadurl in project_dict['urllist']:
                    r=requests.get(downloadurl,stream=True)
                    if os.path.exists(file_path)==False:#目标文件夹如果不存在就重新新建一个
                        os.makedirs('/home/xu/document/longnixfile/'+file_path)
                    #将大文件分块下载
                    with open('/home/xu/document/longnixfile'+downloadurl.replace(urlhead,'').replace(r'/cgit','').replace('snapshot',project_dict['name']),'wb') as down:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                down.write(chunk)
                    # os.system('aria2c ' + downloadurl + ' -o ' + file_path)
                project_branch.append(project_dict)
        item['branch_list'] = project_branch
        yield item