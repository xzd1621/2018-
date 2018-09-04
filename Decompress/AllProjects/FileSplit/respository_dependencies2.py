#根据repository_dependencies.projectid=projects.id &&repository_dependencies.hosttype='Github'
# &&projects.repositoryid=repostories.id &&repostories.hosttype='GitHub'，
# 得到repository_dependencies.name with owner和repository.name with owner，再在它们前面上加上https://github.com./
#得到url,存入本地ｍｏｎｇｏｄｂ的Merged数据库的repository_depend表
#再根据url在opensource_projects表里面得到对应的id
#本来想着在存到mysql,直接多表联合查询，但是mysql屡次崩溃，存到mongodb了

import csv
import time
from multiprocessing.pool import Pool

from pymongo import MongoClient
import pymysql
class importtomysql(object):
    db = pymysql.connect("localhost", "root", "123456", "response_dependency", charset='utf8')
    cursor = db.cursor()
    #将csv复制到ｍｙｓｑｌ里
    #复制ｐｒｏｊｅｃｔｓ表，保留projectsid和responseid
    def importprojects(self):
        with open('/opt/Libraries.io-open-data-1.2.0/use/clean/projects-1.2.0-2018-03-12.csv') as p:
            prreader=csv.reader(p)
            count=0
            for row in prreader:
                count+=1
                idprojects=int(row[0])
                #过滤空字段
                if row[1] !='':
                    responseid=int(row[1])
                else:
                    responseid=-1
                projectssql = "insert into response_dependency.projects values (%s,%s)"#插入mysql
                importtomysql.cursor.execute(projectssql,(idprojects,responseid))
                print('insert'+str(count))
            print('ok')
            importtomysql.db.commit()#提交到数据库，此处千万不能少，否则数据库不会更新sql语句执行的结果
    #复制repository表的reposiyoryid,hosttype,name这三个字段
    def importrepository(self):
        with open('/opt/Libraries.io-open-data-1.2.0/use/clean/repositories-1.2.0-2018-03-12.csv') as p:
            prreader=csv.reader(p)
            count=0
            values=[]
            for row in prreader:
                count+=1
                if count>1:
                    id=int(row[0])
                    hosttype=str(row[1])
                    if len(row[2])<255:
                        name=str(row[2])
                    else:
                        name=''
                    value=(id,hosttype,name)
                    values.append(value)
                print(count)
            try:
                projectssql = "insert into response_dependency.repository values (%s,%s,%s)"
                importtomysql.cursor.executemany(projectssql,values)
                importtomysql.db.commit()
            except Exception as err:
                print(err)
            print('ok')
    #复制dependency_repository表的id,name,hosttype,projectid四个字段
    def importrepositorydepend(self):
        count=0
        for index in range(1, 48):
            with open(
                    '/opt/Libraries.io-open-data-1.2.0/use/clean/repository_dependencies/repository_dependencies-1.2.0-2018-03-12-' + str(
                            index) + '.csv') as p:
                values = []
                prreader=csv.reader(p)
                if(index%10==1):
                    count=0
                for row in prreader:
                    count+=1
                    id=str(row[0])
                    hosttype=str(row[1])
                    if len(row[2])<255:
                        name=str(row[2])
                    else:
                        name=''
                    if row[3] !='':
                        projectid=int(row[3])
                    else:
                        projectid=-1
                    value=(id,hosttype,name,projectid)
                    values.append(value)
                    print(count)
                try:
                    print(index)
                    projectssql="insert into response_dependency.dependencies"+str(int(index/10)+1)+"(`id`,`hosttype`,`name`,`projectid`) values (%s,%s,%s,%s)"
                    importtomysql.cursor.executemany(projectssql,values)
                    importtomysql.db.commit()
                except Exception as err:
                    print(err)
                    time.sleep(10)
                print('ok')
    #讲映射的ｕｒｌ存入mongodb
    #repository_dependencies.projectid=projects.id &&repository_dependencies.hosttype='Github'
    # &&projects.repositoryid=repostories.id &&repostories.hosttype='GitHub'
    def savemongodb(self):
        GITHUB = 'https://github.com/'
        count = 0
        conn=MongoClient('localhost',27017)
        sheet=conn.Merged#Merged数据库
        repository_depend=sheet.repository_depend
        opensource_projects=sheet.opensource_projects
        for index in range(2,6): #dependencies在mysql中一共有五张表,从２开始是因为1运行完了中断过
            desql="select projectid,name from dependencies"+str(index)+" where hosttype='GitHub'" #选择hosttype=github
            importtomysql.cursor.execute(desql)
            deresults = importtomysql.cursor.fetchall()
            for i in deresults:
                pjsql="select responseid from projects where idprojects=%s"
                importtomysql.cursor.execute(pjsql,i[0])#dependencie.projectid=projects.id
                pjresults=importtomysql.cursor.fetchall()
                for j in pjresults:
                    rpsql="select name from repository where hosttype='GitHub' and id=%s"
                    importtomysql.cursor.execute(rpsql,j[0]) #projects.repositoryid=repostories.id
                    rpresults=importtomysql.cursor.fetchall()
                    for k in rpresults:
                        urls=repository_depend.find({"deurl":GITHUB+i[1]},no_cursor_timeout = True)
                        flag=False #防止存入相同的{deurl,reurl}
                        for t in urls:
                            if t["reurl"]==GITHUB+k[0]:
                                flag=True
                                break
                        if flag==False:
                                repository_depend.insert({"deurl":GITHUB+i[1],"reurl":GITHUB+k[0]})
                                count += 1
                                print(str(count) + '*' * 20+str(index))
                                print(GITHUB + i[1])
                                print(GITHUB + k[0])
            print(str(index)+"****")
    #将得到的url映射转化为id的映射
    def urltoid(self):
        count = 0
        conn = MongoClient('localhost', 27017)
        sheet = conn.Merged
        repository_depend = sheet.repository_depend
        # sheet['opensource_projects'].ensure_index([('project_url',1)])#opensource_projects建立projects_url的索引
        repository_dependid = sheet.repository_dependid
        opensource_projects = sheet.opensource_projects
        #在opensource_projects中查找url对应的id
        #将deurl->reurl转化为deid->reid
        for i in repository_depend.find({}):
            depend=opensource_projects.find_one({"project_url":i["deurl"]},no_cursor_timeout = True)
            repository=opensource_projects.find_one({"project_url":i["reurl"]},no_cursor_timeout = True)
            if depend!=None and repository!=None:
                count+=1
                print(str(count)+'*'*20)
                repository_dependid.insert({"dependid":depend["project_id"],"repository":repository["project_id"]})

if __name__ == '__main__':
    # im.importprojects() #2556270
    # im.importrepository() #30705679  (1205, 'Lock wait timeout exceeded; try restarting transaction')
    # im.importrepositorydepend() #231231814  error code:2013 Lost connection to mysql server during
    #result 1:41048575,2:51892421,3:50000000,4:49999997,5:36231814
    im=importtomysql()
    im.savemongodb()
    im.urltoid()