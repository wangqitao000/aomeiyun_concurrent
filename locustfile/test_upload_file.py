# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/29 21:27
@作者 ： 王齐涛
@文件名称： test_rename_folder.py
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from gevent._semaphore import Semaphore
from common.logger_handler import GetLogger
import csv
from pathlib import Path
from locust import HttpUser, TaskSet, task, SequentialTaskSet, User, FastHttpUser, task, constant, events
import base64
import hashlib
import json
from testcase_data.mkdir_files import mkdir_files
from common import all_assert

log = GetLogger()

# 完成在本地创建文件，将生成的文件名保存到csv文件中
log.debug("正在生成测试的数据，请耐心等待！")
share_data = []
name = mkdir_files()
with open(f"./{name}",  newline='') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        share_data.append(row[0])


# 使用信号量的锁，控制获取资源的线程数量，用于并发
all_locusts_spawned = Semaphore()   # 信号量对象
all_locusts_spawned.acquire()   # 获取锁，默认参数（blocking=True, timeout=None）
@events.spawning_complete.add_listener   # Events事件钩子，当所有用户生成时触发，可用于集合点注册
def on_hatch_complete(**kwargs):
    """
    Select_task类的钩子方法
    :param kwargs:
    :return:
    """
    all_locusts_spawned.release()   # 释放锁


# 使用到的变量
header = {"Authorization": "ea7975b76dfa47fd9c10873bc2d5da727e0dc9c592c443388d6fd86ec7b270909bdd64be9b0d4973aa0ab2d8ffa417ba4e6d9ab28fac49e4bd3788f80fa4f124",
          "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
user = 0


class UploadFile(TaskSet):
    """该类用于上传文件"""

    wait_time = constant(1)

    def get_file_path(self):
        """该方法来获取上传文件的路径和并发时生成的用户数，生成全局变量，以此来达到遍历的效果"""
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        file_path = share_data[user]
        log.debug(f"获取到的文件路径：{file_path}")
        return file_path

    def on_start(self):
        """当虚拟用户数为n时，就调用n次，用于并发"""
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态

    def file_shal(self, fullFilePath):
        """
        传入的文件生成hash值是8进制，要通过base64.b64decode(fileHash).hex()转成16进制
        :param fullFilePath: 文件的绝对路径（M:/AOMEIYUNDATA/1234.txt）
        :return: 文件的哈希值，文件的名称，文件的大小
        """
        fileName = Path(fullFilePath)
        # fileName = fullFilePath.split(r"/")[-1]  # 得到文件的名字
        file_state = os.stat(fullFilePath)  # 获取文件的相关信息
        fileSize = file_state.st_size   # 获取文件的大小
        sha1 = hashlib.sha1()
        if file_state.st_size <= 32*1024*1024:
            with open(fullFilePath, 'rb') as f:
                filedata = f.read()
                sha1.update(filedata)
                fileHash = base64.b64encode(sha1.digest()).decode('utf-8 ')
        else:
            with open(fullFilePath, 'rb') as f:
                while True:
                    filedata = f.read(32*1024*1024)
                    if not filedata:
                        break
                    sha1.update(filedata)
            fileHash = base64.b64encode(sha1.digest()).decode('utf-8 ')
        return fileHash, fileName, fileSize

    def get_url(self):
        """获得上传文件的url"""
        file_path = self.get_file_path()
        fileHash, fileName, fileSize = self.file_shal(file_path)  # 调用封装的方法
        print(file_path,fileHash,fileName,fileSize)
        data = {"id": "root", "name": fileName.name, "sha1": base64.b64decode(fileHash).hex(), "size": fileSize}    # 这里的ID不是root，而是专门上传文件的地方
        with self.client.post("/rest/api/basic/upload_url", json=data, headers=header, name="上传文件获得token", verify=False, catch_response=True) as req:
            print(req.text)
            if req.status_code == 200:
                responejson = json.loads(req.text)
                if responejson['data'] is not None and responejson["data"]["url"] is not None:
                    url2 = responejson["data"]["url"]["url2"]
                    token = responejson["data"]["url"]["token"]
                    updata = {"token": token}
                    url = url2 + '?token=' + token
                    return url
                elif responejson['msg'] == 'name_exist':
                    req.failure("File exist!")
                elif responejson['data'] is not None and responejson["data"]["url"] is None:
                    req.success()
                else:
                    req.failure('File update failed!')
            else:
                req.failure("File update failed!")

    @task(1)
    def test_upload_file(self):
        """
        上传文件API
        :param filepath:上传文件的绝对路径
        :return:
        """
        try:
            url = self.get_url()
            file_path = self.get_file_path()
            with open(file_path, 'rb') as f:
                with self.client.post(url, data=f, headers={"Content-Type": "binary"}, name="完成上传文件", verify=False, catch_response=True) as req2:
                    print(req2.text)
                    succeed = "上传文件成功"
                    failure = "上传文件失败"
                    all_assert.all_assert_re(req2, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}")
            raise


class WebsiteUser(HttpUser):    # 不能使用FastHttpUser
    tasks = [UploadFile]
    host = "http://192.168.3.236"


if __name__ == '__main__':
    import os
    os.system("locust -f test_upload_file.py --headless -u 3 -r 1 -t 4s --skip-log-setup")



