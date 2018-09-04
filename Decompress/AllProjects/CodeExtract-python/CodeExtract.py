## extract the function name,function parameter,note,include or import ,class name from a file
##
import hashlib
import re
import os
import json
class File:
    codelist = [] #code in a folder
    filenamelist = [] # filename list
    # read the file ,path is the folder path
    def ReadFile(self, path):
        pathlist = []
        for fpath, dirs, fs in os.walk(path):
            for f in fs:
                pathlist.append(os.path.join(fpath, f))
                File.filenamelist.append(os.path.join(fpath, f).replace(path + '/', ''))
        for fpath in pathlist:
            # print(fpath)
            with open(str(fpath), 'r') as f:
                File.codelist.append(f.read())
        return File.filenamelist,File.codelist #return the filename list and code list in a folder
    def WriteFile(self,filename,name,md5,classname,function,include,notes):
        with open(filename,'a') as f:
            f.write("filename: "+str(name)+"\nmd5: "+str(md5)+"\nclassname:\n"+str(classname)+"\nfunction:\n"+\
                    str(function)+"\ninclude or import or require :\n"+str(include)+"\nnotes:\n"+str(notes)+"\n")
            f.write('**'*50)
class Extract:
    FunctionDict=[] # function dict ,function name: function parameter list
    IncludeList=[]  # include or import list
    NotesList=[]    # note list //.... or /*.....*/
    f="function"
    p="params"
    KeyWord = ['bool', 'char', 'int', 'float', 'double', 'short', 'string', 'void', 'String', 'byte', 'long', 'boolean',
               'public', 'private', 'protected', 'explicit', ';', '~']
    #extract the include or import
    def ExtractInclude(self,code):
        Extract.IncludeList=[]
        pattern=re.compile(r'#include(.*)')
        Extract.IncludeList=pattern.findall(code)
        print('include:',Extract.IncludeList)
    #extract the function
    def ExtractFunctionName(self,code):
            Extract.FunctionDict=[]
            pattern = re.compile(r'((\w+)\s+[\*,&]*\s*(\w+)\s*\((.*?\s*.*?)\s*\))')
            result = pattern.findall(code)
            for i in result:
                if i[2] != 'main':  # exclude the main function
                    for j in Extract.KeyWord:
                        if j in i[1] :
                            d = {}
                            d[Extract.f] = i[2]
                            d[Extract.p] = i[3].replace('\n', '').split(',')
                            Extract.FunctionDict.append(d)
                            break
            Extract.FunctionDict = json.dumps(Extract.FunctionDict)
            print(Extract.FunctionDict)
    #extract the notes
    def ExtractNotes(self,code):
        Extract.NotesList=[]
        pattern=re.compile(r'(\/\/(.*))|(/\*+([\s\S]*?)\*+/)') #match the // or /**/
        result = pattern.findall(code)
        for i in result :
            if i[1]!='':  #match //
                Extract.NotesList.append(i[1])
            if i[3]!='':  #match /**/
                Extract.NotesList.append(i[3].replace('\n',''))
        print('Notes: ',Extract.NotesList)

class CppExtract(Extract):
    ClassList=[]
    #extract the class
    def InKeyword(s):
        for i in CppExtract.KeyWord:
            if i in s:
                return True
        return False
    def ExtractClass(self,code):
        CppExtract.ClassList=[]
        pattern=re.compile(r'class\s+(\w+).*\s*\{')
        result=pattern.findall(code)
        for i in result :
            CppExtract.ClassList.append(i.replace('\n',''))
        print('Class: ',CppExtract.ClassList)
    def ExtractFunctionName(self,code):
        CppExtract.FunctionDict=[]
        for i in CppExtract.ClassList:
            patternFunction = re.compile(r'(.*?)\s+(%s)\s*\((.*?\s*.*?)\)\s*' % i)
            resultFunction = patternFunction.findall(code)
            # add constructor
            if resultFunction != [] :
             for k in resultFunction:
                for j in CppExtract.KeyWord:
                        if CppExtract.InKeyword(k[0]) and (j in k[2] or k[2]==''):
                            d = {}
                            d[CppExtract.f]=i
                            d[CppExtract.p]=k[2].replace('\n','').replace('  ',' ').split(',')
                            CppExtract.FunctionDict.append(d)
                            break
        pattern = re.compile(r'((\w+)\s+[\*,&]*\s*(\w+)\s*\((.*?\s*.*?)\s*\))')
        result = pattern.findall(code)
        for i in result:
            if i[2] != 'main': # exclude the main function
                for j in CppExtract.KeyWord:
                    if j in i[1] and i[2] not in CppExtract.ClassList:
                        d = {}
                        d[CppExtract.f] = i[2]
                        d[CppExtract.p] = i[3].replace('\n', '').replace('  ',' ').split(',')
                        CppExtract.FunctionDict.append(d)
                        break
        CppExtract.FunctionDict=json.dumps(CppExtract.FunctionDict)
        print(CppExtract.FunctionDict)

class JavaExtract(CppExtract):
    def ExtractInclude(self,code):
        Extract.IncludeList = []
        pattern = re.compile(r'import(.*)')
        Extract.IncludeList = pattern.findall(code)
        print('import:', Extract.IncludeList)

class PHPExtract(CppExtract):
    def ExtractInclude(self,code):
        PHPExtract.IncludeList = []
        pattern=re.compile(r'(include_once|include|require_once|require)\s*(.*?);')
        PHPExtract.IncludeList = pattern.findall(code)
        print('include or require:', PHPExtract.IncludeList)
    def ExtractNotes(self,code):
        PHPExtract.NotesList = []
        pattern = re.compile(r'(\/\/(.*))|(/\*+([\s\S]*?)\*+/)|#(.*)')  # match the // or /**/
        result = pattern.findall(code)
        for i in result:
            if i[1] != '':  # match //
                PHPExtract.NotesList.append(i[1])
            if i[3] != '':  # match /**/
                PHPExtract.NotesList.append(i[3].replace('\n', ''))
            if i[4]!='':
                PHPExtract.NotesList.append(i[4])
        print('Notes: ', PHPExtract.NotesList)

    def ExtractFunctionName(self,code):
        PHPExtract.IncludeList=[]
        pattern=re.compile(r'function\s+(.*?)\((.*?)\)\s*{')
        result=pattern.findall(code)
        for i in result:
            d={}
            d[PHPExtract.f]=i[0]
            d[PHPExtract.p]=i[1].split(',')
            PHPExtract.IncludeList.append(d)
        PHPExtract.IncludeList= json.dumps(PHPExtract.IncludeList)
        print(PHPExtract.IncludeList)

if __name__ == '__main__':

    file=File()
    ex = Extract()
    cppex = CppExtract()
    javaex = JavaExtract()
    phpex = PHPExtract()

    filenamelist,codelist=file.ReadFile('/home/xu/document/code/java')
    filename='result.txt'
    print(len(codelist))
    for index,code in enumerate(codelist):

        print('filename:',filenamelist[index])
        MD5=hashlib.md5()
        MD5.update(code.encode("utf-8"))
        print('md5: ',MD5.hexdigest())
        # judge the file
        if '.c' in filenamelist[index]:
            # c
            # Extract.FunctionDict = {}
            ex.ExtractFunctionName(code)
            ex.ExtractInclude(code)
            ex.ExtractNotes(code)
            file.WriteFile(filename,name=filenamelist[index],\
                           md5=MD5.hexdigest(),classname='',function=Extract.FunctionDict\
                           ,include=Extract.IncludeList,notes=Extract.NotesList)

        elif '.cpp' in filenamelist[index] or '.h' in filenamelist[index]:
            # cpp
            # CppExtract.FunctionDict={}
            cppex.ExtractClass(code)
            cppex.ExtractFunctionName(code)
            cppex.ExtractInclude(code)
            cppex.ExtractNotes(code)
            file.WriteFile(filename, name=filenamelist[index], \
                           md5=MD5.hexdigest(), classname=CppExtract.ClassList, function=CppExtract.FunctionDict \
                           , include=CppExtract.IncludeList, notes=CppExtract.NotesList)
        elif '.java' in filenamelist[index]:
            # java
            # JavaExtract.FunctionDict={}
            javaex.ExtractClass(code)
            javaex.ExtractFunctionName(code)
            javaex.ExtractInclude(code)
            javaex.ExtractNotes(code)
            file.WriteFile(filename, name=filenamelist[index], \
                           md5=MD5.hexdigest(), classname=JavaExtract.ClassList, function=JavaExtract.FunctionDict \
                           , include=JavaExtract.IncludeList, notes=JavaExtract.NotesList)
        elif '.php' in filenamelist[index]:
            # PHP
            # PHPExtract.FunctionDict={}
            phpex.ExtractClass(code)
            phpex.ExtractFunctionName(code)
            phpex.ExtractInclude(code)
            phpex.ExtractNotes(code)
            file.WriteFile(filename, name=filenamelist[index], \
                           md5=MD5.hexdigest(), classname=PHPExtract.ClassList, function=PHPExtract.FunctionDict \
                           , include=PHPExtract.IncludeList, notes=PHPExtract.NotesList)
        print('*'*50)