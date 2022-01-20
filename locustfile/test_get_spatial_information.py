# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/31 16:52
@作者 ： 王齐涛
@文件名称： test_check_file_folder.py    ok    ok1
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from common import all_assert
from locust import TaskSet, task, constant, HttpUser, FastHttpUser, events
from gevent._semaphore import Semaphore
from common.logger_handler import GetLogger

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


class GetSpatialInformation(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态

    @task(1)
    def test_check_file(self):
        """获取空间信息(已使用多少内存)"""
        try:
            self.user_index()
            with self.client.post("/rest/api/basic/space", headers=header, name="获取空间信息", verify=False, catch_response=True) as req:
                succeed = "获取空间信息成功"
                failure = "获取空间信息失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}")
            raise


class WebsiteUser(HttpUser):    # 这个不能使用FastHttpUser
    tasks = [GetSpatialInformation]
    host = "http://192.168.3.236"


if __name__ == '__main__':
    import os
    os.system("locust -f test_get_spatial_information.py --headless -u 5 -r 1 -t 6s --skip-log-setup")