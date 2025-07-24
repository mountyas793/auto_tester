# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_api.py
# @Author: Wakka
# @Date: 2025/07/23 20:31
# @Desc: ...
import allure

from utils.runner_utiles import runner
from utils.yaml_utiles import read_yaml


def test_yaml():
    resp = {}
    data = read_yaml()
    allure.title(data["name"])

    for step in data["steps"]:
        print(step)
        for step_name, case_data in step.items():
            runner(step_name, case_data, resp)


if __name__ == "__main__":
    test_yaml()
