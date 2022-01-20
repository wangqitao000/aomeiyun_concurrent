# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/31 16:52
@作者 ： 王齐涛
@文件名称： test_check_file_folder.py  ok   ok1
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


from gevent._semaphore import Semaphore
from common.logger_handler import GetLogger
import json
import queue
import requests
from locust import TaskSet, task, constant, HttpUser, FastHttpUser, events
from common import all_assert

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
    """执行这个locust测试时，循环的次数是某一个目录下的文件或文件夹，所以在设置并发时，要考虑到有多少个文件或文件夹，如果不足，就提前创建文件或文件夹"""
    wait_time = constant(1)
    data = {"id": "root"}
    re1 = requests.post(f"http://192.168.3.236/rest/api/basic/list", json=data, headers=header)  # 调用查看信息接口，获取目录下的文件或文件夹

    def get_file_id(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        file_id = json.loads(self.re1.text)["data"][user]["id"]
        log.debug(f"获取到的文件ID：{file_id}")
        return file_id

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态

    @task(1)
    def test_file_information(self):
        """获取文件或文件夹信息"""
        try:
            file_id = self.get_file_id()
            data = {"id": f"{file_id}"}
            with self.client.post(path="/rest/api/basic/item", headers=header, json=data, name="获取文件或文件夹信息", verify=False, catch_response=True) as req:
                succeed = "获取文件或文件夹信息成功"
                failure = "获取文件或文件夹信息失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}")
            exit(0)
            raise 'account data run out, test ended.'


class WebsiteUser(FastHttpUser):
    tasks = [GetFileInformation]
    host = "http://192.168.3.236"



if __name__ == '__main__':
    import os
    os.system("locust -f test_get_file_folder_information.py --headless -u 5 -r 1 -t 6s --skip-log-setup")