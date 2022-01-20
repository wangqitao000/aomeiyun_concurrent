# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/29 21:27
@作者 ： 王齐涛
@文件名称： test_rename_folder.py   ok
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from gevent._semaphore import Semaphore
from common.logger_handler import GetLogger
from common import all_assert
import json
import queue
import requests
from locust import HttpUser, TaskSet, task, SequentialTaskSet, User, constant, FastHttpUser, events
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


class RenameFile(TaskSet):

    wait_time = constant(1)
    data = {"id": "root"}
    req = requests.post(f"http://192.168.3.236/rest/api/basic/list", json=data, headers=header)  # 调用查看信息接口，获取目录下的文件或文件夹

    def get_file(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        file_id = json.loads(self.req.text)["data"][user]["id"]
        num = random.randint(1, 10000000)
        log.debug(f"获取到的文件ID：{file_id}")
        log.debug(f"获取生成的随机数：{num}")
        return file_id, num

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态

    @task(1)
    def test_rename_file_folder(self):
        """重命名文件或文件夹"""
        try:
            file_id, num_id = self.get_file()
            data = {"id": file_id, "name": f"文件改名{num_id}_{num_id}"}
            with self.client.post(path="/rest/api/basic/rename", json=data, name="重命名文件或文件夹", headers=header, verify=False, catch_response=True) as req:
                succeed = "重命名文件或文件夹成功"
                failure = "重命名文件或文件夹失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}")
            raise


class WebsiteUser(FastHttpUser):
    tasks = [RenameFile]
    host = "http://192.168.3.236"


if __name__ == '__main__':
    import os
    os.system("locust -f test_rename_file_folder.py --headless -u 5 -r 1 -t 5s --skip-log-setup")
