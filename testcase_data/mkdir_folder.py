# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/1/4 12:35
@作者 ： 王齐涛
@文件名称： mkdir_folder.py 
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


csv_path = DATA_PATH+f"/folder{__filename}.csv"  # 构造文件夹的路径
# csv_data = f"文件夹{__filename}+{__folder_name}"      # 构造文件夹的数据
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:    # 这里必须要追加，不然写进csv的文件只有一个
    writer = csv.writer(csvfile)
    for i in range(1, 100):
        num = str(i)
        writer.writerow([num+"文件夹"+num])
    csvfile.close()
