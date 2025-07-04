# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: read_info.py
# @Author: Wakka
# @Date: 2025/07/03 09:17
# @Desc: 读取yaml文件
import json
import os

import yaml

# from dotenv import load_dotenv

# load_dotenv("config/.env")


class YamlReader:
    _cache = {}

    def __init__(self, yaml_file: str = "testData/api_config.yaml"):
        self.yaml_file = yaml_file

    # 读取yaml文件
    def _load_with_cache(self) -> dict:
        """
        读取yaml文件
        :return:
        """
        if self.yaml_file not in self._cache:
            with open(self.yaml_file, encoding="utf-8") as f:
                self._cache[self.yaml_file] = yaml.safe_load(f)
        return self._cache[self.yaml_file]

    def get_data(self) -> dict:
        return self._load_with_cache()

    # 获取接口url
    def get_url(self, api_name: str) -> str:
        """
        获取接口url
        :param api_name: 接口名称
        :return:
        """
        api_config = self.get_data()
        api_info = api_config[api_name]
        host = api_config["host"]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

        return f"{host}{api_info['group']}{api_info['url']}"

    # 获取请求方法
    def get_method(self, api_name: str) -> str:
        """
        获取请求方法
        :param api_name: 接口名称
        :return:
        """
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

        return api_info["method"]

    # 获取请求头
    def get_headers(self, api_name: str, load_env: bool = True) -> dict:
        """
        获取请求头
        :param api_name: 接口名称
        :param load_env: 是否加载环境变量
        :return:
        """
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

        # 处理headers
        headers = api_info["headers"]
        if load_env:
            token = os.environ.get("TOKEN")
            headers["Authorization"] = f"Bearer {token}"
        if headers is None:
            headers = {}
        return headers

    # 获取请求参数
    def get_params(self, api_name: str) -> dict:
        """
        获取请求参数
        :param api_name: 接口名称
        :return:
        """
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]

        # 处理参数
        params = json.dumps(api_info["params"])
        if params is None:
            params = {}
        return params

    # 获取预期结果
    def get_expected(self, api_name: str) -> dict:
        """
        获取预期结果
        :param api_name: 接口名称
        :return:
        """
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]

        expected = api_info["expected"]
        if expected is None:
            expected = {}
        return expected


def main():
    yaml_reader = YamlReader("testData/api_config.yaml")
    print(
        json.dumps(
            yaml_reader.get_headers("selectCwInputInvoicePage"), ensure_ascii=False
        )
    )
    # pass


if __name__ == "__main__":
    main()
