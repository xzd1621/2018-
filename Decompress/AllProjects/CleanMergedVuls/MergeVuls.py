#清洗109上CodeClone的merged_vuls表
#将vul_ids字段和versions下面的vul_ids去重
#原理：先转化为set,再转化为list

from pymongo import MongoClient

class MergeVuls:
    mergevuls=[] #  CodeClone数据库的merged_vuls表
    localmergevuls=[] #本地CodeClone的merged_vuls表
    def connect(self,addr,port): #连接109的CodeClone数据库
        self.conn=MongoClient(addr,port)
        db=self.conn.CodeClone
        MergeVuls.mergevuls=db.merged_vuls

    def connectlocal(self, addr, port): #连接本地的CodeClone数据库
        self.conn = MongoClient(addr, port)
        dblocal = self.conn.CodeClone
        MergeVuls.localmergevuls = dblocal.merged_vuls

    # 复制到本地再处理
    def Copy(self):
        for i in MergeVuls.mergevuls.find({},no_cursor_timeout = True):
            MergeVuls.localmergevuls.insert(i)

    def CleanVulids(self):
        count=0
        for t in MergeVuls.mergevuls.find({},no_cursor_timeout = True):
            count+=1
            if count==1502: #跳过单个文档大于16M的
                i=t #处理versions里面的vul_ids
                if "versions" in i.keys() and len(i["versions"]) > 0:#如果有versions字段
                    for j in range(0, len(i["versions"])):
                        if "vul_ids" in i["versions"][j].keys() and len(i["versions"][j]["vul_ids"]) > 0:#如果versions下面有vuls_ids字段
                            i["versions"][j]["vul_ids"]= list(set(i["versions"][j]["vul_ids"])) # Duplicate removal
                            MergeVuls.mergevuls.update({"project_url": i["project_url"]}, {"$set": {"versions."+str(j)+".vul_ids":i["versions"][j]["vul_ids"]}})
                            print(t["versions"][j]["vul_ids"])
                a=t #处理外部的vul_ids
                if "vul_ids" in a.keys() and len(a["vul_ids"])>0:
                    a["vul_ids"]=list(set(a["vul_ids"]))
                    MergeVuls.mergevuls.update({"project_url": a["project_url"]},
                                               {"$set": {"vul_ids": a["vul_ids"]}})
                    print(t["vul_ids"])
                print(str(count)+"complete!")

if __name__ == '__main__':
    m=MergeVuls()
    m.connect('192.168.1.109',37017)
    m.connectlocal('localhost',27017)
    # m.Copy()
    m.CleanVulids()
    #检测去重结果
    for t in MergeVuls.mergevuls.find({"project_url":"https://github.com/jruby/jruby"}):
            print(t["versions"][0]["vul_ids"])
    print(MergeVuls.mergevuls.count())#1933
    print(MergeVuls.localmergevuls.count())