# -*- coding: utf-8 -*-
import os
import re
import urllib

import scrapy

from scfile.items import ScfileItem

class DownloadfilesSpider(scrapy.Spider):
    name = 'downloadfiles'
    # allowed_domains = ['https://sourceforge.net/directory/?page=1/'] #允许爬取多个网站
    start_urls = ['https://sourceforge.net/directory/?page=1/']

    def sourgehref(hreflist): #正则表达式得到url列表
        dealhreflist=[]
        pattern=re.compile(r'.*href=\"(.*?)\".*')
        for i in hreflist:
            result=pattern.findall(i)
            dealhreflist.append('https://sourceforge.net'+result[0])
        return dealhreflist

    def downloadfile(self,response):
        temp = response.css('.folder').css('a::attr("href")').extract()
        downloadfile=response.css('.file').css('a::attr("href")').extract()
        ##如果是文件夹
        for i in range(len(temp)):
            if 'timeline' not in temp[i] and 'file' in temp[i]:
                filesurl = 'https://sourceforge.net' + temp[i]
                yield scrapy.Request(url=filesurl,callback=self.downloadfile)#递归调用该函数
        ##如果是文件
        if len(downloadfile)>0:
            for i in range(len(downloadfile)):
                if 'download' in downloadfile[i]:
                    downloadurl=downloadfile[i]
                    os.chdir('/home/xu/document/sourceforgefile/')#选择环境默认的文件位置
                    file_name = re.findall(r'.*/(.*?)/download', downloadurl)[0]#匹配文件名字
                    file_path = downloadurl.replace('https://sourceforge.net/projects', '').replace('/files', ''). \
                                    replace('/download', '')#从url中提取出文件的保存路径，使得下载后的目录结构与网站上的相同
                    print(file_name+'*'*20)
                    print(file_path+'&'*20)
                    try:
                        filename = '{}{}{}'.format(file_path, os.sep, file_name)#构建文件的路径＋名字
                        print(filename+'#'*20)
                        # 下载，并保存到文件夹中
                        os.system('aria2c ' + downloadurl + ' -o ' + file_path)#使用ari2ac加快下载速度
                        print('aria2c ' + downloadurl + ' -o ' + file_path)
                    except IOError as e:
                        print('操作失败', e)
                    except Exception as e:
                        print('错误 ：', e)
    def parse(self, response):
        quotes = response.css('.projects')
        item=ScfileItem()
        for quote in quotes:
            urllist = DownloadfilesSpider.sourgehref(quote.css('li').css('.result-heading-texts').css('a').extract())#获取url列表
            namelist = quote.css('li').css('h2::text').extract()#获取名字列表
        for eachurl, eachname in zip(urllist, namelist):
            item['filesurl'] = eachurl.replace('?source=directory', '') + 'files'
            item['name']=eachname
            yield scrapy.Request(item['filesurl'], meta={"url": eachurl, "name": eachname},
                                         callback=self.downloadfile)#将下载链接传入下载函数，使其下载
        next = response.css('.pagination-next a::attr("href")').extract_first()#解析下一页
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)