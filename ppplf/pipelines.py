# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

import pymongo
import docx
import pymysql

from ppp import settings
from scrapy.exporters import CsvItemExporter

class PppPipeline(object):
    # def __init__(self):
    #     # 连接数据库
    #     self.connect = pymysql.connect(
    #         host=settings.MYSQL_HOST,
    #         db=settings.MYSQL_DBNAME,
    #         user=settings.MYSQL_USER,
    #         passwd=settings.MYSQL_PASSWD,
    #         charset='utf8',
    #         use_unicode=True)
    #
    #     # 通过cursor执行增删查改
    #     self.cursor = self.connect.cursor()
    # def process_item(self, item, spider):
    #     wulingshan=['黔江','酉阳','秀山','彭水','武隆','石柱','丰都']
    #     data = dict(item)
    #
    #     flag=True
    #     for i in wulingshan:
    #         if i in item['name'] or i in item['area']:
    #             flag=True
    #             break
    #     file=open("D:\\PycharmProjects\\AllProjects\\ppp\\result.txt",'a')
    #     print(flag)
    #     if flag:
    #         for key,value in data.items():
    #             file.writelines(key)
    #             file.write('\n')
    #             file.writelines(value)
    #             file.write('\n')
    #     file.close()
    #     return item
    def open_spider(self, spider):
        self.file = open("D:\\PycharmProjects\\AllProjects\\ppp\\result.csv", "wb")
        self.file.write(codecs.BOM_UTF8)
        self.exporter = CsvItemExporter(self.file,
                                        fields_to_export=["name", "investment", "area","industry",
                                                          "time","operationmode","mechanism","level","term"
                                                          ,"people","tele","schedule","overview","scope"])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
