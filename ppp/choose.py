import csv

wls=['秭归','长阳','五峰','恩施','利川','建始','巴东','宣恩','咸丰','来凤','鹤峰',
     '新邵','邵阳','隆回','洞口','绥宁','新宁','城步','武冈',
     '石门','慈利','桑植','武陵源','永定','安化',
     '中方','沅陵','辰溪','溆浦','会同','麻阳','新晃','芷江','靖州','鹤城','洪江','通道侗族自治县'
     '新化','涟源','冷水江',
     '泸溪','凤凰','保靖','古丈','永顺','龙山','花垣','吉首',
     '黔江', '酉阳', '秀山', '彭水', '武隆', '石柱', '丰都',
     '正安','道真','务川','凤冈','湄潭','余庆',
     '碧江','江口','玉屏','石阡','思南','印江','德江','沿河','松桃','万山']
province=['湖北','湖南','贵州','重庆']
def choose(csvreadfile,csvwritefile):
     csv_file=csv.reader(open(csvreadfile,'r',encoding='utf-8'))
     out=open(csvwritefile,'a',newline='')
     csv_write=csv.writer(out,dialect='excel')
     count=0
     for row in csv_file:
          count+=1
          print(count)
          flag=False
          print(row)
          for area in wls:
               if len(row)>=3 and (area in row[0] or area in row[2]) and \
                       ('湖北' in row[2] or '湖南' in row[2] or '贵州' in row[2] or '重庆' in row[2]):
                    print(row[0],row[2],area)
                    flag=True
                    break
          if flag:
               print(row)
               csv_write.writerow(row)
if __name__ == '__main__':
    choose('D:\\PycharmProjects\\AllProjects\\ppp\\resultfinance.csv','D:\\PycharmProjects\\AllProjects\\ppp\\choosefinance.csv')