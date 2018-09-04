# -*- coding:utf-8 -*-
#分割文件，避免由于文件过大，处理起来会发生很多问题
#若要更改程序，改source_dir,target_dir，文件名即可
from datetime import datetime

def Main():
    source_dir = '/opt/Libraries.io-open-data-1.2.0/use/repository_dependencies-1.2.0-2018-03-12.csv'
    target_dir = '/opt/Libraries.io-open-data-1.2.0/use/split/repository_dependencies/'

    # 计数器
    flag = 0

    # 文件名
    name = 1

    # 存放数据
    dataList = []

    print("开始。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(source_dir, 'r') as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == 5000000: #满5000000行就存入下一张表
                with open(target_dir + "repository_dependencies-1.2.0-2018-03-12-" + str(name) + ".csv", 'w+') as f_target:
                    for data in dataList:
                        f_target.write(data)
                name += 1
                flag = 0
                dataList = []

    # 处理最后一批行数少于5000000行的
    with open(target_dir + "repository_dependencies-1.2.0-2018-03-12-" + str(name) + ".csv", 'w+') as f_target:
        for data in dataList:
            f_target.write(data)

    print("完成。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    Main()
