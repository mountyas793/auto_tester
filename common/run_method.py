# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: run_method.py
# @Author: Wakka
# @Date: 2025/07/01 21:12
# @Desc: 封装requests请求方法

import requests
from common.prepare_logs import PrepareLogs


class RunMethod(object):
    """
    封装requests请求方法
    """

    def __init__(self) -> None:
        super().__init__()
        self.prepare_logs = PrepareLogs()

    def post_main(self, url: str, headers: dict, json: dict) -> requests.Response:
        """
        post请求
        :param url: 请求url
        :param headers: 请求头
        :param json: 请求参数
        :return:
        """
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        # 遇到requests的ssl验证，若想直接跳过不验证，设置verify=False即可
        response = requests.post(url=url, headers=headers, json=json, verify=False)
        return response

    def get_main(self, url: str, headers: dict, params=None) -> requests.Response:
        """
        get请求
        :param url: 请求url
        :param headers: 请求头
        :param params: 请求参数
        :return:
        """
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=url, headers=headers, params=params, verify=False)
        return response

    def run_main(self, method: str, url: str, headers: dict, data=None) -> dict:
        """
        运行请求
        :param method: 请求方法
        :param url: 请求url
        :param headers: 请求头
        :param data: 请求参数
        :return:
        """
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 5

        if method.upper() == "POST":
            res = self.post_main(url, headers, data)
        elif method.upper() == "GET":
            res = self.get_main(url, headers, data)
        else:
            raise ValueError("不支持的请求方法")
        self.prepare_logs.log_request(method, url, headers, data)
        self.prepare_logs.log_response(res.status_code, res.headers, res.json())
        return res.json()


if __name__ == "__main__":
    run_method = RunMethod()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxNTc1NzE1NzY2NzgyOTk2NDgyIiwicm5TdHIiOiJsM3BKWjBHQ2NPUzFCbVVCWHljZGVjbjlreEtTZUJBWSIsIm1vYmlsZSI6IjE1MDk4MDEwNzA2In0.uNBN558TB0ZkosyCslHy8Zh4uf7R8XLm5ejJk5r-YTw",
    }
    data = {
        "statisticalYear": 2025,
        "statisticalMonth": 7,
    }
    res = run_method.run_main(
        "post",
        "http://192.168.0.80:8080/dev-api/dc-project/cwtaxstatistics/selectCwtaxstatistics",
        headers,
        data,
    )
    # print(res)
