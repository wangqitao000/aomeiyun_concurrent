# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/8 10:32
@作者 ： 王齐涛
@文件名称： mkdir_files.py 
'''
import codecs
import time
from pathlib import Path
from faker import Faker
from os import path
import csv

from common.all_paths import DATA_PATH, LOCUSTFILE_PATH

fake = Faker(locale="zh_CN")    # 调用python的一个库来生成对应的测试数据
__txt_data = fake.texts(nb_texts=3, max_nb_chars=200, ext_word_list=None)  # 生成随机的文章，循环一次是2kb
__filename = fake.random_int()    # 随机数字，默认0~9999，可以通过设置min,max来设置
__folder_name = fake.name()     # 随机生成全名


def mkdir_files():
    """在本地M分区下生成txt文件，以随机的shal值来命名"""
    for i in range(1, 100):   # 循环的次数，表示生成多少个文件夹
        # filename = str(time.time())   # 生成时间戳
        filename = str(fake.sha1())
        filepath = f"M:\\AOMEIYUNDATA\\text\\"+filename + ".txt"  # 文件生成的路径
        with open(filepath, "w") as f:
            csv_name = write_csv(filepath)  # 将路径写入到csv文件中
            for j in range(1, 100):   # 文件中的数据，循环的越多数据就越大
                f.write(f"{__txt_data}+{i}+{j}")
        # print(f"执行了第{i}次,文件名为{filepath}")
    return csv_name


def write_csv(csv_data):
    """写入文件名到CSV文件中"""
    with open(LOCUSTFILE_PATH+f"/testdata{__filename}.csv", "a", newline="", encoding="utf-8") as csvfile:    # 这里必须要追加，不然写进csv的文件只有一个
        writer = csv.writer(csvfile)    # 基于文件对象构建 csv写入对象
        # writer.writerow(["txtName"])  # 构建表头
        writer.writerow([csv_data])     # 写入csv文件类容
        csvfile.close()
    return f"testdata{__filename}.csv"


def read_csv(filepath):
    """读csv文件，将读出的数据添加到data中，返回data"""
    data = []
    with open(filepath) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            data.append(row[0])
    return data





if __name__ == '__main__':
#   mkdir_folder()
    mkdir_files()
    # a = read_csv("../testcase_py/testdata.csv")
    # print(a)
    # print(type(a[0]))
    # b = Path(a[0])
    # # c = b.split(r"\\")[-1]
    # print(b.name)
    # # print(c)

    # # print(a[1].split(r"/"))
    # print(type(a[1]))
    # print(type("M:/AOMEIYUNDATA/1234.txt"))