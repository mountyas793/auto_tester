# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: run_method.py
# @Author: Wakka
# @Date: 2025/07/01 21:12
# @Desc: ...

import requests


class RunMethod(object):
    """
    封装requests请求方法
    """

    def post_main(self, url: str, headers: dict, data: dict) -> requests.Response:
        """
        post请求
        :param url: 请求url
        :param headers: 请求头
        :param data: 请求参数
        :return:
        """
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        # 遇到requests的ssl验证，若想直接跳过不验证，设置verify=False即可
        response = requests.post(url=url, headers=headers, data=data, verify=False)
        return response

    def get_main(self, url: str, headers: dict, data=None) -> requests.Response:
        """
        get请求
        :param url: 请求url
        :param headers: 请求头
        :param data: 请求参数
        :return:
        """
        # 忽略不安全的请求警告信息
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=url, headers=headers, data=data, verify=False)
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
        return res.json()


if __name__ == "__main__":
    run_method = RunMethod()
    res = run_method.run_main("Get", "https://www.baidu.com", None)
    print(res)
