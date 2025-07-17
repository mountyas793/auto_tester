# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: conftest.py
# @Author: Wakka
# @Date: 2025/07/03 10:04
# @Desc: 配置文件

import pytest
from dotenv import load_dotenv

from common.prepare_api import AllApi
from common.read_yaml import YamlReader


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    """
    加载环境变量
    :return:
    """
    load_dotenv("config/.env")


@pytest.fixture(scope="session", autouse=True)
def api_config() -> YamlReader:
    """
    获取yaml文件中的api配置
    :return:
    """
    return YamlReader("testData/api_config.yaml")


@pytest.fixture(scope="function", autouse=True)
def all_api(api_config) -> AllApi:
    """
    获取api配置文件
    :return:
    """
    return AllApi(api_config)


# 添加共享数据fixture
@pytest.fixture(scope="module")
def shared_data():
    return {}


# 测试用例参数化
@pytest.fixture(scope="function")
def api_params(
    request: pytest.FixtureRequest, api_config: YamlReader, shared_data: dict
) -> dict:
    """
    合并YAML配置和共享数据的API请求参数
    :param request: pytest请求对象，用于获取参数化的api_name
    :return: 合并后的请求参数字典
    """
    # 获取参数化的API名称
    api_name = request.param
    if not api_name:
        raise ValueError("API名称不能为空，请通过parametrize传递api_name")

    # 从YAML配置中获取API信息
    api_config_data = api_config.get_info()
    if api_name not in api_config_data:
        raise ValueError(f"API {api_name} 不存在于YAML配置中")

    # 处理YAML中的列表结构，取第一个测试用例配置
    api_info = api_config_data[api_name]
    if isinstance(api_info, list):
        api_info = api_info[0]  # 取列表中的第一个元素

    # 获取基础参数并合并共享数据
    base_params = api_info.get("data", {})
    if not isinstance(base_params, dict):
        base_params = {}

    # 合并共享数据（共享数据优先级更高）
    merged_params = {**base_params, **shared_data}
    return merged_params
