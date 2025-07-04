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

import pytest

from common.app_api import AllApi


@pytest.mark.parametrize("api_name", ["selectCwtaxstatistics"])
def test_select_statistics_valid(api_name: str, api_config):
    """
    测试查询年度，月税费接口
    :param api_name: 接口名称
    :return:
    """
    all_api = AllApi(api_config)
    res = all_api.send_request(api_name)
    expect = all_api.get_expect(api_name)
    assert res["code"] == expect["code"], (
        f"code: {res['code']}, 预期结果: {expect['code']}"
    )
    assert res["msg"] == expect["msg"], f"msg: {res['msg']}, 预期结果: {expect['msg']}"


def main():
    test_select_statistics_valid("selectCwtaxstatistics")
    # pass


if __name__ == "__main__":
    pytest.main()
