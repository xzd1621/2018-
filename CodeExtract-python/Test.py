import json
# d1={}
# key=1
# value=2
# d1.setdefault(key,set()).add(value)
# value=2
# d1.setdefault(key,set()).add(value)
# value=3
# d1.setdefault(key,set()).add(value)
# print(d1)
# a=[]
# f="function"
# p="params"
# d={}
# d[f]="asda"
# d[p]="s,asd,asd,qwe,1234,1234,weq,tr,gh".split(',')
# a.append(d)
# d[f]="sda"
# d[p]="bv,342,fd,6,gf,7,56".split(',')
# a.append(d)
# print(a)
# a=json.dumps(a)
# print(a)
# KeyWord=['bool','char','int','float','double','short','string','void','String','byte','long','boolean','public','private','protected','explicit',';','~']
# for j in KeyWord:
#     if j in 'public:':
#         print(j)
# from pymongo import MongoClient
# conlocal=MongoClient('localhost',27017)
# mergeddb = conlocal.Merged
# projcollectionmerged = mergeddb.opensource_projects
# count39=0;count40=0;countother=0;count0=0
# d={}
# for i in range(30,50):
#     d[i]=0
# for i in projcollectionmerged.find({}, no_cursor_timeout=True):
#         t=len(i)
#         d[t]+=1
#         # if t==39:
#         #     count39+=1
#         #     print(str(count39)+'*'*20)
#         # elif t==40:
#         #     count40+=1
#         #     print(str(count40)+'*'*40)
#         #     print(i)
#         #     break
#         # else:
#         #     countother += 1
#         #     print(str(countother) + '*' * 60)
#
#         print(d)
import re

xmlstring='<metadata>\n  <groupId>academy.alex</groupId>\n  <artifactId>custommatcher</artifactId>\n  <versioning>\n    <latest>1.0</latest>\n    <release>1.0</release>\n    <versions>\n      <version>1.0</version>\n    </versions>\n    <lastUpdated>20180531190143</lastUpdated>\n  </versioning>\n</metadata>'
pattern=re.compile(r'.*<groupId>(.*?)</groupId>\s*.*<artifactId>(.*?)</artifactId>.*')
result=pattern.findall(xmlstring)
print(result[0][0])
print(result[0][1])
# MavenSpider.item['groupid']=result[0][0]
# MavenSpider.item['artifactid']=result[0][1]


