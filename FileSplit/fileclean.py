#从已经被分割的文件中提取出需要的字段
#repository表中的id,hosttype,name with owner
# projects表的id,repository id
# repository_dependencies的id,hosttype name with owner, project id
#三个表的提取都是由这个程序完成，只需对表名和选择的第几行进行改变即可。
import csv
csv.field_size_limit(500 * 1024 * 1024)#防止csv文件过大
datalist = []
with open('/opt/Libraries.io-open-data-1.2.0/use/clean/projects-1.2.0-2018-03-12.csv', 'w', newline='') as c:
    with open('/opt/Libraries.io-open-data-1.2.0/use/projects-1.2.0-2018-03-12.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            temp = []
            temp.append(row[0])
            temp.append(row[-1])
            datalist.append(temp)

        writer=csv.writer(c)
        writer.writerows(datalist)