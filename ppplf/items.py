# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PppItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() #项目名字
    investment=scrapy.Field()#项目总投资
    area=scrapy.Field()#所在地区
    industry=scrapy.Field()#所属行业
    time=scrapy.Field()#发起时间
    operationmode=scrapy.Field()#项目运作方式
    mechanism=scrapy.Field()#回报机制
    level=scrapy.Field()#项目示范级别/批次
    term=scrapy.Field()#合作期限
    people=scrapy.Field()#联系人
    tele=scrapy.Field()#联系电话
    schedule=scrapy.Field()#项目进度
    overview=scrapy.Field()#项目概况
    scope=scrapy.Field()#项目合作范围

