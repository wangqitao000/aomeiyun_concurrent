# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/31 17:41
@作者 ： 王齐涛
@文件名称： delete_folder_or_file.py 
'''
import json
import requests
header = {"Authorization": "ea7975b76dfa47fd9c10873bc2d5da727e0dc9c592c443388d6fd86ec7b270909bdd64be9b0d4973aa0ab2d8ffa417ba4e6d9ab28fac49e4bd3788f80fa4f124",
          "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}


# 批量删除文件夹
data = {"id": "root"}

# 获取该目录下的所有文件或文件夹
re1 = requests.request(url="http://192.168.3.236/rest/api/basic/list", method="post", json = data , headers=header)
print(re1.text)
a = json.loads(re1.text)["data"]
for i in range(len(a)):
    b = json.loads(re1.text)["data"][i]["id"]
    name = json.loads(re1.text)["data"][i]["name"]
    if "txt" in name:   # 匹配name中含有“文件夹”的文件夹
        data = {"id": f"{b}"}
        re5 = requests.request(url="http://192.168.3.236/rest/api/basic/delete", method="post", json=data, headers=header)
        print(re5.text)
        print(i)