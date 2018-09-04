from pymongo import MongoClient
conn=MongoClient('localhost',27017)
dblocal = conn.CodeClone
localmergevuls = dblocal.merged_vuls
count=0
Except=[1360,1380]
for t in localmergevuls.find({},no_cursor_timeout = True):
            count+=1
            if count==1502:
                i=t
                if "versions" in i.keys() and len(i["versions"]) > 0:
                    for j in range(0, len(i["versions"])):
                        if "vul_ids" in i["versions"][j].keys() and len(i["versions"][j]["vul_ids"]) > 0:
                            i["versions"][j]["vul_ids"]= list(set(i["versions"][j]["vul_ids"]))
                            localmergevuls.update({"project_url": i["project_url"]}, {"$set": {"versions."+str(j)+".vul_ids":i["versions"][j]["vul_ids"]}})
                            print(t["versions"][j]["vul_ids"])
                a=t
                if "vul_ids" in a.keys() and len(a["vul_ids"])>0:
                    a["vul_ids"]=list(set(a["vul_ids"]))
                    localmergevuls.update({"project_url": a["project_url"]},
                                               {"$set": {"vul_ids": a["vul_ids"]}})
                    print(t["vul_ids"])
                print(str(count)+"complete!")