import os
import re
class zip():
    countcorrect = 0
    countall = 0
    dictfile = {}
    def removedup(self,filepath):
        for root,dirs,files in os.walk(filepath):
            zip.countall+=len(files)
            filecorrect=0
            wrongfile=[]
            for file in files:
                match = re.search(r'.*?.zip$',file)
                if match:
                    filecorrect+=1
                else:
                    wrongfile.append(file)
            zip.countcorrect+=filecorrect
            if filecorrect!=len(files) and len(files)!=0:
                zip.dictfile[root]=wrongfile
    def savemysql(self):
        import pymysql
        db = pymysql.connect("localhost", "root", "123456", "codeclone2", charset='utf8')
        cursor = db.cursor()
        for path,files in zip.dictfile.items():
            for file in files :
                insql="insert into codeclone2.duplicatefile(`path`,`filename`) values (%s,%s)"
                cursor.execute(insql,(path,file))
                db.commit()

if __name__ == '__main__':

    z=zip()
    z.removedup('/opt/927442')
    z.savemysql()