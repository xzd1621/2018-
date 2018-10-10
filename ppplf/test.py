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

from xlutils.copy import copy
w =copy('book1.xls')
w.get_sheet(0).write(0,0,"foo")
w.save('book2.xls')