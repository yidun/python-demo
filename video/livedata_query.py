#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务视频直播截图结果查询接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python livedata_query.py
"""
__author__ = 'yidun-dev'
__date__ = '2020/04/28'
__version__ = '0.2-dev'

import hashlib
import time
import random
import urllib.request as urlrequest
import urllib.parse as urlparse
import json


class LiveDataQueryByTaskIdDemo(object):
    """视频直播截图结果查询接口示例代码"""

    API_URL = "http://as.dun.163.com/v1/livevideo/query/image"
    VERSION = "v1.1"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff.encode("utf8")).hexdigest()

    def query(self,params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.gen_signature(params)

        try:
            params = urlparse.urlencode(params).encode()
            request = urlrequest.Request(self.API_URL, params)
            content = urlrequest.urlopen(request, timeout=10).read()
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = LiveDataQueryByTaskIdDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    # 私有请求参数
    params = {
        "taskId": "c633a8cb6d45497c9f4e7bd6d8218443",
        "levels": "[1,2]",
        "callbackStatus": "1",
        "pageNum": "1",
        "pageSize": "10"
    }

    ret = api.query(params)

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        result: dict = ret["result"]
        status: int = result["status"]
        images: dict = result["images"]
        count: int = images["count"]
        rows: list = images["rows"]
        if status == 0:
            for row in rows:
                url: str = row["url"]
                label: int = row["label"]
                labelLevel: int = row["labelLevel"]
                callbackStatus: int = row["callbackStatus"]
                beginTime: int = row["beginTime"]
                endTime: int = row["endTime"]
            print("live data query success, images: %s" % rows)
        elif status == 20:
            print("taskId is expired")
        elif status == 30:
            print("taskId is not exist")
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
