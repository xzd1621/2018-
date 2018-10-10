# # -*- coding: utf-8 -*-
# """
# Created on Tue Oct  9 19:58:05 2018
#
# @author: 西风烈
# """
#
# import docx
# #获取文档对象
# file=docx.Document("D:\\BUAA\\大三上\\操作系统\\第一次课前作业.docx")
# print("段落数:"+str(len(file.paragraphs)))#段落数为13，每个回车隔离一段
#
# #输出每一段的内容
# for para in file.paragraphs:
#     print(para.text)
#
# #输出段落编号及段落内容
# for i in range(len(file.paragraphs)):
#     print("第"+str(i)+"段的内容是："+file.paragraphs[i].text)

# wulingshan=['黔江','酉阳','秀山','彭水','武隆','石柱','丰都']
# s='重庆彭水至酉阳高速公路'
# for i in wulingshan:
#     if i in s:
#         print(i)

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = "Hm_lvt_42d4e52241c499f01129fbc4079ad9cb=1539072595; Hm_lpvt_42d4e52241c499f01129fbc4079ad9cb=1539105089"
    trans = transCookie(cookie)
    print (trans.stringToDict())