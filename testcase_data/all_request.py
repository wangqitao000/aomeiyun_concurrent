# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/28 12:27
@作者 ： 王齐涛
@文件名称： all_request.py
'''
import json
import requests
header = {"Authorization":"ea7975b76dfa47fd9c10873bc2d5da727e0dc9c592c443388d6fd86ec7b270909bdd64be9b0d4973aa0ab2d8ffa417ba4e6d9ab28fac49e4bd3788f80fa4f124","Accept":"*/*","Content-Type":"application/json","Connection":"Close"}
# 基本API




# 列目录下的文件和文件夹
data = {"id": "root"}
re1 = requests.request(url = "http://192.168.3.236/rest/api/basic/list", method="post", json = data , headers=header)
print(re1.text)
print(len(json.loads(re1.text)["data"]))
print(json.loads(re1.text)["data"][0]["id"])





# data = {"id": "root", "name": "文件夹6"}     # root是为一级目录
# re2 = requests.request(url = "http://192.168.3.236/rest/api/basic/mkdir", method="post", json = data , headers=header)
#      # 创建文件夹
# print(type({"msg":"success"})) ["data"]["id"]
# a= json.loads(re2.text)["data"]["id"]
# print(a)
# print(type(a))




# 删除文件或文件夹
# if "success" in str(re2.text):
#     print(re2.text)
#     print(type(json.loads(re2.text)["data"]["id"]))
# a=json.loads(re2.text)["data"]["id"]
# data = {"id": f"{a}"}
# re5 = requests.request(url = "http://192.168.3.236/rest/api/basic/delete", method="post", json=data, headers=header)
# print(re5.text)




# 重命名文件或文件夹
# data = {"id": "5415ec68252c48bcbbe90e142ed44536", "name": "文件夹一改为文件夹二"}
# re3 = requests.request(url = "http://192.168.3.236/rest/api/basic/rename", method="post", json = data , headers=header)
# print(re3.text)




# 获取空间信息
# re4 = requests.request(url = "http://192.168.3.236/rest/api/basic/space", method="post",headers=header)
# print(re4.text)




# 获取文件或文件夹信息
# data = {"id": "d83887d815f34750b853a46c2de4eca7"}
# re6 = requests.request(url = "http://192.168.3.236/rest/api/basic/item", method="post", json=data, headers=header)
# print(re6.text)




# 大文件下载获取网址
# data = {"id": "7dd97a91a99143f3952920aeed087537"}
# re6 = requests.request(url = "http://192.168.3.236/rest/api/basic/download_url", method="post", json=data, headers=header)
# print(re6.text)





# 大文件上传获取网址
# data = {
#     "id": "root",
#     "name": "ac-core-1.0.jar",
#     "sha1": "8a3520396a13b61e20f7595ae7dd8da420b29ff1",
#     "size": 69217852,
#     "state": ""
# }
# re7 = requests.request(url = "http://192.168.3.236/rest/api/basic/space", method="post", json=data, headers=header)
# print(re7.text)







# 用户API


# 用户api，响应结果为id和token
# data = {"key": "", "param": ""}
# re8 = requests.request(url = "http://192.168.3.236/rest/api/user/auth", method="post", json=data, headers=header)
# print(re8.text)

