# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_api.py
# @Author: Wakka
# @Date: 2025/07/23 20:31
# @Desc: ...
import allure

from common.runner_utiles import runner
from common.yaml_utiles import load_yaml


def test_yaml():
    my_var = {}
    data = load_yaml("testData/test_api.yaml")
    allure.title(data["name"])

    for step in data["steps"]:
        print(step)
        for k, v in step.items():
            runner(k, v, my_var)


if __name__ == "__main__":
    test_yaml()
