# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_select_statistics.py
# @Author: Wakka
# @Date: 2025/07/02 16:42
# @Desc: 查询年度，月税费
"""
POST /cwtaxstatistics/selectCwtaxstatistics
接口ID：209619092
接口地址：https://app.apifox.com/link/project/5068016/apis/api-209619092
请求参数：
{
    "statisticalYear": 2025,
    "statisticalMonth": 7
}
响应参数：
{
    "code": 0,
    "data": {},
    "msg": "string"
}
"""

import json

import pytest

from common.run_method import RunMethod

runMethod = RunMethod()


@pytest.mark.parametrize(
    "data",
    [
        {"statisticalYear": 2025, "statisticalMonth": 7},
        {},
        {"statisticalMonth": 6},
        {"statisticalMonth": "dsafgjkl 是打发"},
    ],
)
def test_select_statistics(data: dict):
    api = "cwtaxstatistics/selectCwtaxstatistics"
    baseUrl = "http://192.168.0.80:8080/dev-api/dc-project/"
    url = baseUrl + api
    method = "Post"
    data = json.dumps(data)
    header = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxNTc1NzE1NzY2NzgyOTk2NDgyIiwicm5TdHIiOiJRMjd6YTRpd3RTSU9QamEzMFB3aEcyOW83VHFDQ3B1YiIsIm1vYmlsZSI6IjE1MDk4MDEwNzA2In0.eK92PD67jkg-oNBO-45cTeA5kd2iNekSsxbQYgXDvz8",
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Host": "192.168.0.80:8080",
        "Connection": "keep-alive",
    }
    res = runMethod.run_main(method, url, header, data)
    assert res.status_code == 200


def main():
    test_select_statistics()


if __name__ == "__main__":
    main()
