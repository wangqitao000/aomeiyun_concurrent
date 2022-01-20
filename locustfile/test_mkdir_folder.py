# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/29 21:27
@作者 ： 王齐涛
@文件名称： test_rename_folder.py    ok
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from gevent._semaphore import Semaphore
from common.logger_handler import GetLogger
import json
import requests
from common import all_assert
from locust import HttpUser, TaskSet, task, SequentialTaskSet, User, task, constant, FastHttpUser, events
import random


all_locusts_spawned = Semaphore()   # 于控制获取资源的线程数量
all_locusts_spawned.acquire()
@events.spawning_complete.add_listener
def on_hatch_complete(**kwargs):
    """
    Select_task类的钩子方法
    :param kwargs:
    :return:
    """
    all_locusts_spawned.release()


header = {"Authorization": "ea7975b76dfa47fd9c10873bc2d5da727e0dc9c592c443388d6fd86ec7b270909bdd64be9b0d4973aa0ab2d8ffa417ba4e6d9ab28fac49e4bd3788f80fa4f124",
          "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
user = 0
log = GetLogger()


class MkdirFolder(TaskSet):

    wait_time = constant(1)

    def get_num(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        num = random.randint(1, 1000000000)
        log.debug(f"获取随机数：{num}")
        return num

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态

    @task(1)
    def test_mkdir_folder(self):
        """创建文件夹"""
        try:
            num_id = self.get_num()
            data = {"id": "root", "name": f"{num_id}文件夹{num_id}"}     # root为一级目录
            print(f"创建文件夹{data}")
            with self.client.post(path="/rest/api/basic/mkdir", json=data, headers=header, name="创建文件夹", verify=False, catch_response=True) as req:
                succeed = "创建文件夹成功"
                failure = "创建文件夹失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}")
            raise


class WebsiteUser(FastHttpUser):
    tasks = [MkdirFolder]
    host = "http://192.168.3.236"


if __name__ == '__main__':
    import os
    os.system("locust -f test_mkdir_folder.py --headless -u 5 -r 1 -t 5s --skip-log-setup")
