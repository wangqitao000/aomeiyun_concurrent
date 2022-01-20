# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/1/5 16:53
@作者 ： 王齐涛
@文件名称： test2.py 
'''
from threading import Thread
import threading

lock = threading.Lock()
def sub_thread3():
    for i in range(100):
        lock.acquire()
        print('this is sub_thread3') # 锁将print函数变得具有“原子性”
        lock.release()

def sub_thread4():
    for i in range(100):
        lock.acquire()

        lock.release()
        print('this is sub_thread4') # 锁将print函数变得具有“原子性”

t3 = Thread(target=sub_thread3,)
t4 = Thread(target=sub_thread4,)
t3.start()
t4.start()