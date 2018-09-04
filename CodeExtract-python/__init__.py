import requests
import os
import urllib
# print ("downloading with requests")
# url = 'https://sourceforge.net/projects/hyperestraier/files/hyperestraier/1.4.13/hyperestraier-1.4.13.tar.gz/download'
# r = requests.get(url)
# with open("hyperestraier-1.4.13.tar.gz", "wb") as code:
#      code.write(r.content)
import cmd


def save_img(img_url,file_name,file_path='book\img'):
#保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
     try:
          if not os.path.exists(file_path):
               print('文件夹',file_path,'不存在，重新建立')
               os.makedirs(file_path)
          #获得图片后缀
          # file_suffix = os.path.splitext(img_url)[1]
          #拼接图片名（包含路径）
          filename = '{}{}{}'.format(file_path,os.sep,file_name)
          #下载图片，并保存到文件夹中
          urllib.request.urlretrieve(img_url,filename=filename)
     except IOError as e:
          print ('文件操作失败',e)
     except Exception as e:
          print ('错误 ：',e)
if __name__ == '__main__':
    file_path='/home/xu/document/sourceforgefile/myimg'
    img_url='https://sourceforge.net/projects/clonezilla/files/clonezilla_live_doc/OldFiles/QuickReference_Card_0.9.3/ClonezillaLiveRefCard_FR_0.9.3.pdf/download'
    # save_img(img_url,'ClonezillaLiveRefCard_FR_0.9.3.pdf',file_path=file_path)
    img_name='ClonezillaLiveRefCard_FR_0.9.3.pdf'
    os.chdir('/home/xu/document/sourceforgefile/')
    os.system('aria2c '+img_url+' -o '+'/a/b/'+img_name)
    # cmdline.execute(('aria2c '+img_url+' -o '+'document/sourceforgefile/'+img_name).split())

