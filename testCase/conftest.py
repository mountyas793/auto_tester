# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: conftest.py
# @Author: Wakka
# @Date: 2025/07/03 10:04
# @Desc: 配置文件

import pytest
from dotenv import load_dotenv

from utils.yaml_utils import yaml_to_dict


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    """
    加载环境变量
    :return:
    """
    load_dotenv("config/.env")


@pytest.fixture(scope="session")
def test_data() -> dict:
    """
    加载测试数据
    :return:
    """
    return yaml_to_dict()
