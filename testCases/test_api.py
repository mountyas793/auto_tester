# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_api.py
# @Author: Wakka
# @Date: 2025/07/23 20:31
# @Desc: 测试用例，用于测试接口，根据测试用例的yaml文件，调用运行器，实现不同的功能
import allure
import pytest
from conftest import test_data

from utils.runner_utils import runner


@pytest.mark.parametrize("test_yaml", ["test_api.yaml"])
def test_yaml(data: test_data):
    resp = {}
    allure.title(data["name"])

    for step in data["steps"]:
        print(step)
        for step_name, case_data in step.items():
            runner(step_name, case_data, resp)


if __name__ == "__main__":
    test_yaml()
