# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: read_info.py
# @Author: Wakka
# @Date: 2025/07/03 09:17
# @Desc: 读取yaml文件
import json
import os

import yaml
from dotenv import load_dotenv

load_dotenv("config/.env")


class YamlReader:
    _cache = {}

    def __init__(self, yaml_file: str = "testData/api_config.yaml"):
        self.yaml_file = yaml_file

    def _load_with_cache(self) -> dict:
        if self.yaml_file not in self._cache:
            with open(self.yaml_file, encoding="utf-8") as f:
                self._cache[self.yaml_file] = yaml.safe_load(f)
        return self._cache[self.yaml_file]

    def get_data(self) -> dict:
        return self._load_with_cache()

    def get_url(self, api_name: str) -> str:
        api_config = self.get_data()
        api_info = api_config[api_name]
        host = api_config["host"]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

        return f"{host}{api_info['group']}{api_info['url']}"

    def get_method(self, api_name: str) -> str:
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

        return api_info["method"]

    def get_headers(self, api_name: str) -> dict:
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

        headers = api_info["headers"]
        token = os.environ.get("TOKEN")
        headers["Authorization"] = f"Bearer {token}"
        if headers is None:
            headers = {}
        return headers

    def get_params(self, api_name: str) -> dict:
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

        params = json.dumps(api_info["params"])
        if params is None:
            params = {}
        return params

    def get_expected(self, api_name: str) -> dict:
        api_config = self.get_data()
        api_info = api_config[api_name]
        if not isinstance(api_info, (dict, list)):
            raise ValueError(f"Invalid api_info type: {type(api_info)}")

        if isinstance(api_info, list):
            api_info = api_info[0]  # 取第一个元素

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
