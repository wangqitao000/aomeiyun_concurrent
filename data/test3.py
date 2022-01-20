# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/1/5 17:16
@作者 ： 王齐涛
@文件名称： test3.py 
'''
import time
import threading


def sub():
    global num
    num -= 1
    time.sleep(1)
num = 100  # 定义一个全局变量
l = []  # 定义一个空列表，用来存放所有的列表
for i in range(100):  # for循环100次
    t = threading.Thread(target=sub)  #每次循环开启一个线程
    t.start()  # 开启线程
    l.append(t)  # 将线程加入列表l
for i in l:
    i.join()  # 这里加上join保证所有的线程结束后才运行下面的代码
print(num)