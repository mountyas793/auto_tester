# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_select_statistics.py
# @Author: Wakka
# @Date: 2025/07/02 16:42
# @Desc: 查询年度，月税费

import pytest
from common.prepare_api import AllApi


class TestSelectStatistics:
    @pytest.mark.parametrize("api_name", ["selectCwtaxstatistics"])
    def test_select_statistics_valid(self, api_name: str, api_config):
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
        assert res["msg"] == expect["msg"], (
            f"msg: {res['msg']}, 预期结果: {expect['msg']}"
        )


def main():
    test = TestSelectStatistics()
    test.test_select_statistics_valid("selectCwtaxstatistics")
    # pass


if __name__ == "__main__":
    pytest.main()
