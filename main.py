# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: main.py
# @Author: Wakka
# @Date: 2025/07/03 09:57
# @Desc: ...
import os

import dotenv

dotenv.load_dotenv("config/.env")


# 生成测试报告
if __name__ == "__main__":
    os.system("pytest -s -v testCases/ --alluredir=report/allure-results")
    os.system("allure generate  report -o report/allure-results")
    os.system("allure open report/allure-results")
