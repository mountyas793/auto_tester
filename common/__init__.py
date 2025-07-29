# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: __init__.py
# @Author: Wakka
# @Date: 2025/07/24
# @Desc: common模块初始化文件


"""通用模块包，包含配置、日志、数据库等公共功能"""

__all__ = [
    "ConfigReader",
    "CommonLogger",
    "DbClient",
    "HttpClient",
    "PathManager",
    "build_allure_report",
    "case_read",
]

# 先导入基础模块（无外部依赖的）
from .allure_builder import build_allure_report
from .case_reader import case_read
from .common_logger import CommonLogger
from .config_reader import ConfigReader

# 再导入依赖基础模块的模块
from .db_client import DbClient
from .http_client import HttpClient
from .path_manager import PathManager
