# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: conftest.py
# @Author: Wakka
# @Date: 2025/07/03 10:04
# @Desc: 配置文件

import pytest

from utils.yaml_utils import read_yaml


@pytest.fixture(scope="session")
def test_data() -> dict:
    """加载测试数据"""
    return read_yaml("testData/api_config.yaml")
