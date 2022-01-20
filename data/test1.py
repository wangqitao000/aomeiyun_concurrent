# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/1/5 16:51
@作者 ： 王齐涛
@文件名称： test1.py 
'''
from threading import Thread


def sub_thread3():
    for i in range(100):
        print('this is sub_thread3')

def sub_thread4():
    for i in range(100):
        print('this is sub_thread4')

t3 = Thread(target=sub_thread3)
t4 = Thread(target=sub_thread4)
t3.start()
t4.start()