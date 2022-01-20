# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/1/4 20:41
@作者 ： 王齐涛
@文件名称： monitor.py 
'''
import psutil
import time



print("CPU使用率  内存使用率  C盘使用率")
while True:
    time.sleep(3)
    print(psutil.cpu_percent(), psutil.virtual_memory().percent, psutil.disk_usage(r'C:\\').percent)
