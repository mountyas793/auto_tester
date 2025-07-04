# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: app_api.py
# @Author: Wakka
# @Date: 2025/07/03 11:02
# @Desc: 接口集合
import json

from common.run_method import RunMethod
from common.yaml_reader import YamlReader


class AllApi:
    def __init__(self, api_config: YamlReader):
        self.run = RunMethod()
        self.api_config = api_config

    def send_request(self, api_name: str) -> dict:
        try:
            # 获取接口请求参数
            url = self.api_config.get_url(api_name)
            method = self.api_config.get_method(api_name)
            headers = self.api_config.get_headers(api_name)

            # 判断请求方法
            if method.upper() == "GET":
                res = self.run.run_main(method, url, headers)
            elif method.upper() == "POST":
                params = self.api_config.get_params(api_name)
                res = self.run.run_main(method, url, headers, params)
            print(
                "url: %s, method: %s, headers: %s, params: %s"
                % (
                    url,
                    method,
                    headers,
                    json.dumps(params, ensure_ascii=False, sort_keys=False),
                )
            )
            print(
                json.dumps(
                    res["msg"], indent=2, ensure_ascii=False, sort_keys=False
                )
            )
            return res

        except Exception as e:
            print("接口访问出错啦~ %s" % e)
            # self.logger.info("接口访问出错啦~ %s" % e)
            return None

    def get_expect(self, api_name: str) -> dict:
        try:
            # 获取yaml文件中的预期结果
            expect = self.api_config.get_expected(api_name)
            if expect is None:
                raise ValueError("接口 %s 的预期结果为空" % api_name)
            return expect
        except Exception as e:
            print("获取预期结果出错啦~ %s" % e)
            # self.logger.info("获取预期结果出错啦~ %s" % e)
            return None


def main():
    yaml_reader = YamlReader("testData/api_config.yaml")
    all_api = AllApi(yaml_reader)
    res = all_api.send_request("selectCwtaxstatistics")
    # print(res)


if __name__ == "__main__":
    main()
