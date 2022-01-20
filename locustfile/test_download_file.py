# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/31 16:52
@作者 ： 王齐涛
@文件名称： test_check_file_folder.py  ok
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from common.logger_handler import GetLogger
import json
import queue
import requests
from locust import TaskSet, task, constant, HttpUser, FastHttpUser, events
from common import all_assert
from gevent._semaphore import Semaphore


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


class GetFileInformation(TaskSet):
    wait_time = constant(1)
    data = {"id": "b7d35d57e87e4b1aa5d408698c565339"}
    re1 = requests.post(f"http://192.168.3.236/rest/api/basic/list", json=data, headers=header)  # 调用查看信息接口，获取目录下的文件或文件夹

    def get_file(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        print(f"第{user}个虚拟用户开始启动!")
        file_id = json.loads(self.re1.text)["data"][user]["id"]
        print(self.re1.text)
        log.debug(f"获取到的文件ID：{file_id}")
        print(f"获取到的文件ID：{file_id}")
        return file_id

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态

    @task(1)
    def test_file_information(self):
        """大文件下载获取网址"""
        try:
            file_id = self.get_file()   # 获取队列中的数据
            data = {"id": f"{file_id}"}
            print(data)
            with self.client.post(path="/rest/api/basic/download_url", headers=header, json=data, name="获取文件下载网址", verify=False, catch_response=True) as req:
                print(req.text)
                succeed = "大文件下载获取网址成功"
                failure = "大文件下载获取网址失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}")
            raise


class WebsiteUser(FastHttpUser):
    tasks = [GetFileInformation]
    host = "http://192.168.3.236"



if __name__ == '__main__':
    import os
    os.system("locust -f test_download_file.py --headless -u 10 -r 1 -t 10s --skip-log-setup")