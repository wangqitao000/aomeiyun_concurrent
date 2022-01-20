# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/31 16:52
@作者 ： 王齐涛
@文件名称： test_check_file_folder.py    ok
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))  # 特别注意这个必须放在最前面。解决pytyhon的包引用的处理的问题，如果不要这个，调用封装函数的时候就会报错


from gevent._semaphore import Semaphore
from locust import TaskSet, task, constant, FastHttpUser, events
from common import all_assert
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


class CheckFile(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_check_file_folder(self):
        """查看列目录下的文件或文件夹"""
        try:
            self.user_index()
            data = {"id": "root"}
            with self.client.post(path="/rest/api/basic/list", json=data, headers=header, name="查看列目录下的文件或文件夹", verify=False, catch_response=True) as req:
                succeed = "查看列目录下的文件或文件夹成功"
                failure = "查看列目录下的文件或文件夹失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。可能是列表索引超出范围，列表中没有文件或文件夹了")
            raise "IndexError: list index out of range!"


class WebsiteUser(FastHttpUser):
    tasks = [CheckFile]
    host = "http://192.168.3.236"


if __name__ == '__main__':
    import os
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")



#  --headless -u 10 -r 1 -t 11s   表示10+(11-10)*10=20个虚拟用户    u+(t-u)*u=用户数（其中t>=u）
