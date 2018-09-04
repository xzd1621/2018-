#Merge the bitbuckets ,opensource_projects in CodeClone and opensource_projects inCodeClone3
#功能：合并CodeClone的bitbuckets ,opensource_projects和CodeClone3的opensource_projects这三张表
#合并原则：选择versions长度更长的，如果相同的id,对应的字段有的表有，有的没有，就合并在一起
#结果：合并后的大小为54510610，存入109的CodeCloneWhole
from pymongo import MongoClient
class Bin():
    projcollection3=[]  #codeclone3 opensource_projects
    projcollection =[] #codeclone opensource_projects
    projcollectionbitbuckets=[] #codeclone bitbuckets
    projcollectionmerged=[] #merged  the final result
    insertcount=0 # the count of insert
    updatecount=0 # the count of update
    def __init__(self,addr,port):
        self.addr=addr
        self.port=port
    #connect
    def connect(self):
        self.conn = MongoClient(self.addr, self.port)  # connect mongodb
        # CodeClone3
        db3 = self.conn.CodeClone3
        Bin.projcollection3 = db3.opensource_projects

        # CodeClone
        db = self.conn.CodeClone
        Bin.projcollection = db.opensource_projects
        Bin.projcollectionbitbuckets = db.bitbuckets
    def close(self):
        if self.mongoClient is not None:
            self.mongoClient.close()
    #连接本地数据库
    def connectlocal(self,addr,port):
        self.connlocal=MongoClient(addr,port)
        # Merged Database
        mergeddb = self.connlocal.Merged
        Bin.projcollectionmerged = mergeddb.opensource_projects

    #拷贝到本地的Merged数据库
    def Add(self,set):
        Bin.insertcount=0
        for i in set.find({}):
            Bin.projcollectionmerged.insert(i)
            Bin.insertcount += 1
            print("insert!" + str(Bin.insertcount))

    @classmethod
    def MergePlus(self,set):
            count=0
            for j in set.find({},no_cursor_timeout = True):
                if count!=715932: #跳过大于16M的
                    # 在Merged数据库里面找相同的project_id
                    i=Bin.projcollectionmerged.find_one({"project_id":j["project_id"]},no_cursor_timeout = True)
                    # 如果找不到就直接插入
                    if i==None:
                        Bin.projcollectionmerged.insert(j)
                        Bin.insertcount += 1
                        print("insert!" + str(Bin.insertcount))
                    # 找得到就合并
                    else:
                        # 选择versions字段更长的
                        if "versions" in i.keys() and "versions" in j.keys() and  len(j["versions"]) > len(i["versions"]):
                            Bin.projcollectionmerged.update({"project_id": i["project_id"]},
                                                            {"$set": {"versions": j["versions"]}})
                            Bin.updatecount += 1
                            print("update!" + str(Bin.updatecount) + "-project_id: " + str(i["project_id"]))
                            i["versions"] = j["versions"]
                        # 如果本来的表的文档没有要合并的表文档里面的字段，就加进去
                        for key, value in j.items():
                            if key not in i:
                                Bin.projcollectionmerged.update({"project_id": i["project_id"]}, {"$set": {key: value}})
                                Bin.updatecount += 1
                                print("update!" + str(Bin.updatecount) + "-project_id: " + str(i["project_id"]))
                    print("the size of Merged is:" + str(Bin.projcollectionmerged.count()))
                count+=1
                print("*"*50+str(count))
            print("size: " + str(set.count()) + " Merged success!")
    @classmethod
    #去除不需要的字段，给缺省的字段添加默认值
    def AddDefault(self,set):
        adddefault=0 #the count of add default value
        # 需要添加缺省值的字段
        DefaultValue = {
            "project_user": -1,
            "created_time": "",
            "main_language": "",
            "project_name": "",
            "latest_version": "",
            "last_version_time": "",
            "official_license": [],
            "versions": [],
            "project_fork": 0,
            "project_watch": 0,
            "project_star": 0,
            "full_name": "",
            "is_library": 0,
            "detail_info": "",
            "project_desc": "",
            "homepage": "",
            "popularity_level": 0,
            "popularity": 0,
            "svn_url": "",
            "git_url": "",
            "ssh_url": "",
            "watching": 0,
            "maintance": 0,
            "contributors": 0,
            "activity_score": 0,
            "frequency": 0,
            "use_friendly_score": 0,
            "vul_high": 0,
            "vul_mid": 0,
            "vul_low": 0,
            "vul_unknown": 0,
            "security": 0,
            "project_userid": 0,
            "project_commits":0,
            "project_issues":0,
            "version_num": 0,
        }
        # 不需要的字段，前面几个已去，所以注释
        AbundonValue={
            # "vul_info": "",
            # "versions_total": 0,
            # "highest_risk": 0,
            # "vul_details": "",
            # "is_update": 0,
            #"is_fork": "false",
            "is_download":0,
            "visited":0,
            "fork_updated":0,
            "eariliest_version_time":"",
            "visited_flag":0,
            "visited_flag2":0,
            "project_contributors":0,
        }
        # 去除不需要的字段，由于已经运行过，所以注释
        # for key in AbundonValue:
        #     set.update({}, {"$unset": {key: ""}}, multi=True)
        #     print(key)
        # add the needed field
        count=0
        for i in set.find({},no_cursor_timeout = True):
            if count>32000000:#之前运行过，此处16M，所以跳过
                for key, value in DefaultValue.items():
                    if key not in i or i[key] is None:
                        set.update({"project_id": i["project_id"]}, {"$set": {key: value}})
                        adddefault += 1
                        print("AddDefault:" + str(adddefault))
            count+=1
            print(str(count)+'*'*100)

    def Removepro(self,set):
        set.remove()


if __name__ == '__main__':
    con=Bin('192.168.1.109',37017)
    con.connect()
    con.connectlocal('localhost',27017)
    #都已经运行过，所以注释
    # con.Removepro(Bin.projcollectionmerged)
    # con.Add(Bin.projcollection)
    #con.MergePlus(Bin.projcollectionbitbuckets)
    #con.MergePlus(Bin.projcollection3)
    #
    # con.AddDefault(Bin.projcollectionmerged)

    print(Bin.projcollectionmerged.count())#54510610
    print(Bin.projcollection3.count()) #1115133
    print(Bin.projcollectionbitbuckets.count()) #1367034
    print(Bin.projcollection.count()) #53215178