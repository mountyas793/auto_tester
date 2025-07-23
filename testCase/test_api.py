# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_api.py
# @Author: Wakka
# @Date: 2025/07/23 20:31
# @Desc: ...
import allure

from common.read_yaml import load_yaml
from common.runner_utiles import runner


def test_yaml():
    my_var = {}
    data = load_yaml("testCase/test_api.yaml")
    allure.title(data["name"])

    for step in data["steps"]:
        for k, v in step.items():
            runner(k, v, my_var)
