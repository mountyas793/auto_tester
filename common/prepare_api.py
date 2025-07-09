# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: prepare_api.py
# @Author: Wakka
# @Date: 2025/07/03 11:02
# @Desc: 接口集合

from common.read_yaml import YamlReader
from common.run_method import RunMethod


class AllApi(object):
    """
    接口集合
    """

    def __init__(self, api_config: YamlReader):
        """
        初始化接口集合
        :param api_config: 接口配置文件
        """
        self.run = RunMethod()
        self.api_config = api_config

    def send_request(self, api_name: str) -> dict:
        """
        发送请求
        :param api_name: 接口名称
        :return: 接口响应数据
        """
        try:
            # 获取接口请求参数
            url = self.api_config.get_url(api_name)
            method = self.api_config.get_method(api_name)
            headers = self.api_config.get_headers(api_name)

            # 判断请求方法
            if method.upper() == "GET":
                res = self.run.run_main(method, url, headers)
            elif method.upper() == "POST":
                data = self.api_config.get_data(api_name)
                res = self.run.run_main(method, url, headers, data)
            return res

        except Exception as e:
            print("接口访问出错啦~ {}".format(e))
            return None

    def get_expect(self, api_name: str) -> dict:
        """
        获取预期结果
        :param api_name: 接口名称
        :return: 预期结果
        """
        try:
            # 获取yaml文件中的预期结果
            expect = self.api_config.get_expected(api_name)
            if expect is None:
                raise ValueError("接口 {} 的预期结果为空".format(api_name))
            return expect
        except Exception as e:
            print("获取预期结果出错啦~ {}".format(e))
            return None


def main():
    read_yaml = YamlReader("testData/api_config.yaml")
    all_api = AllApi(read_yaml)
    res = all_api.send_request("selectCwtaxstatistics")
    # print(res)


if __name__ == "__main__":
    main()
