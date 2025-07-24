# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: http_client.py
# @Author: Wakka
# @Date: 2025/07/24 15:07
# @Desc: 封装 requests 库，提供更方便的接口


from typing import Any, Dict

import requests
from http_logger import HttpLogger


class HttpClient(object):
    def __init__(self):
        self.session = requests.Session()
        self.logger = HttpLogger()  # 单例

    def send_request(self, **kwargs: Dict[str, Any]) -> requests.Response:
        """
        case_spec 必须包含：
        method, url, headers, data/json/body(可选)
        """
        # 提取参数
        method = kwargs["method"].upper()
        url = kwargs["url"]
        headers = kwargs.get("headers", {})
        body = kwargs.get("data") or kwargs.get("json") or kwargs.get("body")

        # 记录请求
        self.logger.log_request(method, url, headers, body)
        # print(
        #     f"[DEBUG] 发送请求……\nmethod: {method}\nurl: {url}\nheaders: {headers}\nbody: {body}"
        # )

        # 真正发送
        resp = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=body if isinstance(body, (dict, list)) else None,
            data=None if isinstance(body, (dict, list)) else body,
            timeout=10,
        )

        # 记录响应
        try:
            resp_json = resp.json()
        except ValueError:
            resp_json = resp.text
        self.logger.log_response(resp.status_code, dict(resp.headers), resp_json)
        # print(
        #     f"[DEBUG] 响应状态码：{resp.status_code}\n响应头：{dict(resp.headers)}\n响应体：{resp_json}"
        # )

        return resp_json


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv("config/.env")
    from yaml_utils import _load_yaml, _replace_env

    data = _replace_env(_load_yaml("testData/test_api.yaml")["steps"][0]["request"])
    session = HttpClient()
    resp = session.send_request(**data)
