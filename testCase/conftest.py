# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: conftest.py
# @Author: Wakka
# @Date: 2025/07/03 10:04
# @Desc: 配置文件

import pytest
from common.read_yaml import YamlReader
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    """
    加载环境变量
    :return:
    """
    load_dotenv("config/.env")


@pytest.fixture(scope="module", autouse=True)
def api_config() -> YamlReader:
    """
    获取api配置文件
    :return:
    """
    return YamlReader("testData/api_config.yaml")
