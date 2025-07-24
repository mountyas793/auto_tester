# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: main.py
# @Author: Wakka
# @Date: 2025/07/03 09:57
# @Desc: ...
import os

# 生成测试报告
os.system("allure generate -c -o report --clean")
