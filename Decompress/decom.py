import os
import zipfile

import rarfile

class decom():
    def delmkdir(self,path):
        for root,dirs,files in os.walk(path):
            print(root,dirs,files)
            for file in files:
                if file.endswith('.rar'):
                    dirpath=path+'\\'+file.replace('.rar','')
                    rar=rarfile.RarFile(path+'\\'+file)
                    if os.path.isdir(dirpath):
                        pass
                    else:
                        os.mkdir(dirpath)
                    rar.extract(path)
                    rar.close()
                    os.remove(path+'\\'+file)
                    self.delmkdir(dirpath)
                elif file.endswith('.zip'):
                    dirpath=path+'\\'+file.replace('.zip','')
                    zip=zipfile.ZipFile(path+'\\'+file)
                    if os.path.isdir(dirpath):
                        pass
                    else:
                        os.mkdir(dirpath)
                    for z in zip.namelist():
                        zip.extract(z,dirpath.replace('\\'+file.replace('.zip',''),''))
                    zip.close()
                    os.remove(path+'\\'+file)
                    self.delmkdir(dirpath)
                elif file.endswith('.tar') or file.endswith('.tar.gz'):
                    dirpath=path+'//'+file.replace('.')

if __name__ == '__main__':
    de=decom()
    de.delmkdir(r'D:\PycharmProjects\testdecom')