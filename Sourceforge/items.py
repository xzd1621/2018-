# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SourceforgeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field() #项目地址
    name=scrapy.Field() #项目名称
    introduce_brief=scrapy.Field() #项目的简介1
    introduce_detail=scrapy.Field() #项目的简介2
    svnurl=scrapy.Field() #项目code地址
    giturl=scrapy.Field() #项目code地址
    filesurl=scrapy.Field() #项目files地址
    comment=scrapy.Field() #项目评论数量
    downloads=scrapy.Field() #下载量
    last_update_time=scrapy.Field() #最近更新时间
    star=scrapy.Field() #项目评分
    language=scrapy.Field() #项目语言
    license=scrapy.Field() #项目license
    codelanguage=scrapy.Field() #项目编程语言
    category=scrapy.Field() #项目类别


