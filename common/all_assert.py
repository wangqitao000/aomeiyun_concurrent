# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/1/4 16:48
@作者 ： 王齐涛
@文件名称： all_assert.py 
'''
from common.logger_handler import GetLogger

log = GetLogger()


def all_assert_re(req, succeed, failure):
    if "success" in str(req.text):
        req.success()
        log.debug(f"请求成功的结果: {req.text}")
        log.debug(succeed)
    elif "name_exist" in str(req.text):
        log.error(f"添加失败，该名称已存在：{req.text}")
        req.failure("请求失败")
    elif req.status_code == 401:
        log.error(f"报错提示：401  Unauthorized。可能是传入的headers错误或者没传")
        req.failure("Unauthorized!")
    elif req.status_code == 403:
        log.error(f"报错提示：403  Forbidden。")
        req.failure("Forbidden!")
    elif req.status_code == 404:
        log.error(f"报错提示：404  Not Found。")
        req.failure("Not Found!")
    else:
        log.error(f"请求失败的结果: {req.text}")
        req.failure(failure)