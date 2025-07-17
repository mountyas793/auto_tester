# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: read_yaml.py
# @Author: Wakka
# @Date: 2025/07/03 09:17
# @Desc: 读取yaml文件
import os
from typing import Any

import yaml


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

    # 获取API配置信息，自动处理列表结构
    def get_api_info(self, api_name: str) -> dict:
        """
        获取API配置信息，自动处理列表结构
        :param api_name: API名称
        :return: API配置信息
        """
        api_config = self._load_with_cache()
        if api_name not in api_config:
            raise ValueError(f"API {api_name} not found in YAML configuration")

        api_info = api_config[api_name]
        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个测试用例配置

        if not isinstance(api_info, dict):
            raise ValueError(f"API {api_name} configuration is not a dict")
        return api_info

    # 添加通用配置获取方法
    def get_config_value(self, api_name: str, key: str, default: Any = None) -> Any:
        api_info = self.get_api_info(api_name)
        return api_info.get(key, default)

    # 获取接口url
    def get_url(self, api_name: str, load_env: bool = True) -> str:
        """
        获取接口url
        :param api_name: 接口名称
        :return:
        """
        api_group = self.get_config_value(api_name, "url")
        api_url = self.get_config_value(api_name, "url")

        if load_env:
            host = os.environ.get("HOST")
            base_url = "{}{}{}".format(host, api_group, api_url)

        return base_url

    # 获取请求方法
    def get_method(self, api_name: str) -> str:
        """
        获取请求方法
        :param api_name: 接口名称
        :return:
        """
        method = self.get_config_value(api_name, "method")
        return method

    # 获取请求头
    def get_headers(self, api_name: str, load_env: bool = True) -> dict:
        """
        获取请求头
        :param api_name: 接口名称
        :param load_env: 是否加载环境变量
        :return:
        """
        headers = self.get_config_value(api_name, "headers")
        if load_env:
            token = os.environ.get("TOKEN")
            headers["Authorization"] = "Bearer {}".format(token)
        if headers is None:
            headers = {}
        return headers

    # 获取请求参数
    def get_data(self, api_name: str) -> dict:
        """
        获取请求参数
        :param api_name: 接口名称
        :return:
        """
        data = self.get_config_value(api_name, "data")
        if data is None:
            data = {}
        return data

    # 获取预期结果
    def get_expected(self, api_name: str) -> dict:
        """
        获取预期结果
        :param api_name: 接口名称
        :return:
        """
        expected = self.get_config_value(api_name, "expected")
        if expected is None:
            expected = {}
        return expected

    # 更新接口请求参数
    def set_data(self, api_name: str, data: dict) -> None:
        """
        更新接口请求参数

        :param api_name: API名称
        :type api_name: str
        :param data: 新的请求参数
        :type data: dict
        :raises ValueError: 当API名称不存在时抛出
        :raises TypeError: 当data不是字典类型时抛出
        """
        if not isinstance(data, dict):
            raise TypeError(
                f"Expected dict type for data, got {type(data).__name__} instead"
            )

        # 复用get_api_info处理配置获取和类型检查
        api_info = self.get_api_info(api_name)
        api_info["data"] = data

        # 更新缓存（保持原数据结构）
        api_config = self._load_with_cache()
        if isinstance(api_config[api_name], list):
            api_config[api_name][0] = api_info
        else:
            api_config[api_name] = api_info
        self._cache[self.yaml_file] = api_config


def main():
    import dotenv

    dotenv.load_dotenv("config/.env")
    read_yaml = YamlReader("testData/api_config.yaml")
    # # 测试get_info
    # print(read_yaml.get_info()["AddMaterialCategory"])
    # 测试get_url
    print(read_yaml.get_url("AddMaterialCategory"))
    # # 测试get_method
    # print(read_yaml.get_method("AddMaterialCategory"))
    # # 测试get_headers
    # print(json.dumps(read_yaml.get_headers("AddMaterialCategory"), ensure_ascii=False))
    # # 测试get_expected
    # print(json.dumps(read_yaml.get_expected("AddMaterialCategory"), ensure_ascii=False))
    # # 测试get_data
    # print(json.dumps(read_yaml.get_data("AddMaterialCategory"), ensure_ascii=False))
    # pass


if __name__ == "__main__":
    main()
