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


@pytest.fixture(scope="session", autouse=True)
def _load_dotenv():
    # 加载环境变量
    load_dotenv("config/.env")


@pytest.fixture(scope="session")
def project_path() -> str:
    """获取项目目录"""
    project_name = "auto_tester"  # auto_tester为项目名称
    file_path = os.path.dirname(__file__)  # 获取当前路径
    # print("当前路径:", file_path)
    project_path = file_path[
        : file_path.find(project_name) + len(project_name)
    ]  # 截取项目路径
    return project_path


@pytest.fixture(scope="session")
def test_data() -> dict:
    """加载测试数据"""
    return case_read("testData/api_config.yaml")


@pytest.fixture(scope="session")
def db_client() -> DbClient:
    """创建数据库客户端"""
    return DbClient()
