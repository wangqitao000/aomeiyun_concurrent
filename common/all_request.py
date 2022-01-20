# -*- encoding: utf-8 -*-
"""
@时间:   2021/11/7 16:12
@作者:   王齐涛
@文件:   all_request.py
定义请求的一个入口，方便做统计
"""



def all_send_request(self, url, method, data, heander,**kwargs):
    try:
        method = str(method).lower()   # 将传入的参数全部转换为小写
        if method == "post":
            # strdata= json.dumps(data)   将格式转为字符串,这里不需要，传进来的就是字符串
            # print(method, url, data)
            with self.client.post(url=url, json=data, allow_redirects=False, **kwargs) as res:
                return res
        elif method == "get":
            with self.client.get(url=url, json=data, allow_redirects=False, **kwargs) as res2:
                return res2
        else:
            print("你输入的参数有误，不支持的请求方式")
    except Exception:
        raise ConnectionError("可能是服务器没有开或者网络异常")




