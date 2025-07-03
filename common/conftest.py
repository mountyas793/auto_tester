# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: conftest.py
# @Author: Wakka
# @Date: 2025/07/03 10:04
# @Desc: 配置文件

import pytest
from dotenv import load_dotenv

from common.yaml_reader import YamlReader


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    load_dotenv("config/.env")


@pytest.fixture(scope="module")
def api_config() -> YamlReader:
    return YamlReader("testData/api_config.yaml")
