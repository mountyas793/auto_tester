# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: conftest.py
# @Author: Wakka
# @Date: 2025/07/03 10:04
# @Desc: 配置文件

import os

import pytest
from dotenv import load_dotenv

from ..common.case_reader import case_read
from ..common.db_client import DbClient
from ..common.config_reader import ConfigReader

@pytest.fixture(scope="session", autouse=True)
def _load_dotenv():
    # 加载环境变量
    load_dotenv("config/.env")


@pytest.fixture(scope="session")
def test_data() -> dict:
    """加载测试数据"""
    return case_read("testData/api_config.yaml")


@pytest.fixture(scope="session")
def db_client() -> DbClient:
    """创建数据库客户端"""
    return DbClient()

@pytest.fixture(scope="session")
def config_reader() -> ConfigReader:
    """创建配置读取器"""
    return ConfigReader()

@pytest.fixture(scope="session")
def log_config(config_reader) -> dict:
    """获取日志配置"""
    return config_reader.get_log_config()