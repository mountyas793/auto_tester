# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: main.py
# @Author: Wakka
# @Date: 2025/07/03 09:57
# @Desc: ...
import os

import pytest
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv("config/.env")

# 生成测试报告
os.system("allure generate -c -o report temps")

# 执行测试
pytest.main(["-s", "test_cases"])

# 打开测试报告
os.system("allure open report")
