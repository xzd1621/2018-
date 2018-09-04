# 清洗artifacts表，存入本地，已经复制到109的CodeCloneWhole
#将表中的license和versions下面的字段赋值为codeclone2.license中的值
#并且前后两个值字符串相似度最大
#外层原来的license是licenseoriginal,新值为license
#versions内层原值是license,新值为licenseplus
#字符串相似度计算方法：编辑距离，动态规划思想
from pymongo import MongoClient
import pymysql
class CleanMaven():
    art=[] # maven.artifacts表
    artlocal=[] # Merged.artifacts表
    copycount=0 #the count of copy
    # 连接到maven数据库
    def ConnectMaven(self,addr,port):
        self.conn=MongoClient(addr,port)
        dbmaven=self.conn.CodeClone
        CleanMaven.art=dbmaven.vul_projects
    def ConnectMysql(self):
        pass
    #连接到Merged数据库
    def Connectlocal(self,addr,port):
        self.connlocal=MongoClient(addr,port)
        mergeddb = self.connlocal.CodeCloneWhole
        CleanMaven.artlocal=mergeddb.vul_projects
    #复制到本地的 Merged.artifacts
    def copy(self,set):
        CleanMaven.copycount=0
        for i in set.find({}):
            CleanMaven.art.insert(i)
            CleanMaven.copycount+= 1
            print("insert!" + str(CleanMaven.copycount))
    #由于赋新值之前忘了给外层的license备份，所以后来再插入原来的值，即licenseoriginal
    def AddOriginal(self,set):
        count=0
        for i in set.find({},no_cursor_timeout = True):
            if "license" in i.keys() and len(i["license"]) > 0 and count>118101:
                CleanMaven.artlocal.update({"url": i["url"]}, {"$set": {"licenseOriginal": i["license"]}})
            count+=1
            print(count)
    # 备份veriosns里层的license
    def AddLicense(self,set):
        count=0
        for i in set.find({},no_cursor_timeout=True):
            if "versions" in i.keys() and len(i["versions"])>0 and count>118101: #跳过单个文件大于16M的
                for j in range(0,len(i["versions"])):
                    if "license" in i["versions"][j].keys() and len(i["versions"][j]["license"])>0:
                        CleanMaven.artlocal.update({"url": i["url"]}, {"$set": {"versions." + str(j)+".licensePlus": i["versions"][j]["license"]}})
            count += 1
            print(count)

    # 处理外层的license，外层处理方法是数据库的模糊匹配
    def dealOutlicense(self):
        db = pymysql.connect("localhost", "root", "123456", "codeclone2", charset='utf8')
        cursor = db.cursor()
        count=0
        for i in CleanMaven.artlocal.find({},no_cursor_timeout = True):
            if "license" in i.keys() and len(i["license"])>0:
                for j in range(0,len(i["license"])):
                    args = '%' + i["license"][j] + '%'
                    sqlcount = "select count(*) from codeclone2.license where simname like '%s'" % args# 模糊匹配
                    try:
                        cursor.execute(sqlcount)
                        resultscount = cursor.fetchall()
                        if resultscount[0][0]>1: # 匹配结果不止一个就先跳过
                            continue
                        elif resultscount[0][0]==1:#匹配结果只有一个就更新
                            sqlname = "select simname from codeclone2.license where simname like '%s'" % args
                            try:
                                cursor.execute(sqlname)
                                resultsname = cursor.fetchall()
                                CleanMaven.artlocal.update({"url":i["url"]}, {"$set": {"license."+str(j):resultsname[0][0]}})
                                count+=1
                                print("update"+str(count)+"!")
                            except:
                                print("Error1")
                    except:
                        print("Error2")
        db.close()

    # 计算字符串相似度，动态规划算法
    @classmethod
    def Levenshtein(self,sm,sn):
        m,n=len(sm)+1,len(sn)+1
        matrix=[[0]*n for i in range(m)]
        matrix[0][0]=0
        for i in range(1,m):
            matrix[i][0]=matrix[i-1][0]+1
        for i in range(1,n):
            matrix[0][i]=matrix[0][i-1]+1
        cost=0
        for i in range(1,m):
            for j in range(1,n):
                if sm[i-1]==sn[j-1]:
                    cost=0
                else:
                    cost=1
                matrix[i][j]=min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+cost)
        return 1-(matrix[m-1][n-1]/max(m-1,n-1))


    #处理｀versions内层的license
    def dealInnerlicense(self):
        db = pymysql.connect("localhost", "root", "123456", "codeclone2", charset='utf8')
        cursor = db.cursor()
        updatecount=0
        for i in CleanMaven.artlocal.find({},no_cursor_timeout = True):
            if "versions" in i.keys() and len(i["versions"])>0:
                for indexj,j in enumerate(i["versions"]):
                     if "licensePlus" in j.keys() and len(j["licensePlus"]) >0:
                            for indexk,k in enumerate(j["licensePlus"]):
                                if type(k) is dict and "name" in k.keys():
                                    artname=k["name"]
                                    artsql = "select name,name_without_version from codeclone2.license"
                                    maxLevenshtein=0
                                    try:
                                        # 从codeclone2.license里面选择字符串相似度最高的
                                        cursor.execute(artsql)
                                        results = cursor.fetchall()
                                        for i2 in range(len(results)):
                                            for j2 in range(len(results[0])):
                                                if CleanMaven.Levenshtein(results[i2][j2],artname)>maxLevenshtein:
                                                    maxLevenshtein=CleanMaven.Levenshtein(results[i2][j2],artname)
                                                    maxstr=results[i2][j2]
                                        CleanMaven.artlocal.update({"url": i["url"]},
                                                                   {"$set": {"versions." + str(indexj)+".licensePlus."+str(indexk)+".name": maxstr}})
                                        # print(maxstr)
                                        # print(maxLevenshtein)
                                        updatecount+=1
                                        print("update:"+str(updatecount))
                                    except:
                                        print("Error:unable to fetch data")
        db.close()

if __name__ == '__main__':
    clean=CleanMaven()
    clean.ConnectMaven('192.168.3.99',37017)
    clean.Connectlocal('192.168.1.109',37017)
    clean.copy(CleanMaven.artlocal)
    # clean.dealOutlicense()
    # clean.AddOriginal(CleanMaven.art)
    # clean.AddLicense(CleanMaven.art)
    # clean.dealInnerlicense()