import re
import os
class CExtract():
    codelist=[]
    filenamelist=[]
    def ReadFile(self,path):
        pathlist=[]
        for fpath, dirs, fs in os.walk(path):
            for f in fs:
                pathlist.append(os.path.join(fpath, f))
                print(os.path.join(fpath, f))
                CExtract.filenamelist.append(os.path.join(fpath, f).replace(path+'/',''))
        for fpath in pathlist:
            # print(fpath)
            with open(str(fpath),'r') as f:
                CExtract.codelist.append(f.read())
                # print(f.read())
    def ExtractInclude(self,code):
        pattern=re.compile(r'(#include.*)')
        result=pattern.findall(code)
        print('include:',result)
    def ExtractFunctionName(self,code):
            pattern=re.compile(r'((\w+)\s+[\*,&]*\s*(\w+)\s*\((.*)\)\n*\{)')
            result=pattern.findall(code)
            for i in result:
                if i[2]!='main':
                    print('function name:',i[2])
                    print('function parameter list:',i[3])
            # print(result)
    # def ExtractNotes(self,code):
    #     pattern=re.compile(r'(\/\/(.*))|(/\*+([\s\S]*?)\*+/)')
    #     result = pattern.findall(code)
    #     for i in result :
    #         if i[1]!='':
    #
    #     print(result)


if __name__ == '__main__':
    CE=CExtract()
    CE.ReadFile('/home/xu/document/code/c')
    for index,i in enumerate(CE.codelist):
        print('filename:',CE.filenamelist[index])
        CE.ExtractInclude(i)
        CE.ExtractFunctionName(i)
        # CE.ExtractNotes(i)
        print(i)
        print('*' * 50)