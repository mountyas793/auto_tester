# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_api.py
# @Author: Wakka
# @Date: 2025/07/23 20:31
# @Desc: 测试用例，用于测试接口，根据测试用例的yaml文件，调用运行器，实现不同的功能
import allure

from ..utils.runner_utils import runner
from .conftest import test_data


def test_yaml(test_data):
    resp = {}
    allure.title(test_data["name"])

    for step in test_data["steps"]:
        for step_name, case_data in step.items():
            runner(step_name, case_data, resp)


if __name__ == "__main__":
    test_yaml(test_data)
