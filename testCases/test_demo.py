# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_api.py
# @Author: Wakka
# @Date: 2025/07/23 20:31
# @Desc: 测试用例，用于测试接口，根据测试用例的yaml文件，调用运行器，实现不同的功能
import allure

from ..utils.runner_utils import runner


@allure.description("线索管理列表查询-成功")
@allure.epic("CRM系统")
@allure.feature("线索管理")
@allure.story("数据查询")
@allure.tag("查询")
def test_selectCrmCluePage(test_data, log_config):
    resp = {}
    allure.title(test_data["name"])

    for step in test_data["steps"]:
        for step_name, case_data in step.items():
            print(f"step_name: {step_name}")
            with allure.step(step_name):
                runner(step_name, case_data, resp, log_config)


if __name__ == "__main__":
    pass
