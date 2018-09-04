# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoongnixItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    project_name=scrapy.Field()#项目名字
    project_url=scrapy.Field()#项目链接
    project_description=scrapy.Field()#项目描述
    branch_list=scrapy.Field()#branch的列表，[名字:name,下载链接列表:[url],作者:author,年龄:age]
    pass
