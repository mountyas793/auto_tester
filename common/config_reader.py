# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: config_reader.py
# @Author: Wakka
# @Date: 2025/07/23 20:11
# @Desc: 读取项目配置文件，支持环境变量替换

import os
from functools import lru_cache

import yaml

from .common_logger import CommonLogger
from .path_manager import PathManager


class ConfigReader:
    def __init__(self, config_name: str = "config.yaml"):
        """初始化配置读取器"""
        self.project_path = PathManager()
        self.logger = CommonLogger()
        self.config_path = self.project_path.get_path("base.config") / config_name
        self._config = None

    @lru_cache(maxsize=1)
    def env_config_read(self) -> dict:
        """读取项目环境变量, 并缓存结果"""
        self.logger.log_info(f"读取配置文件路径: {self.config_path}")

        with open(self.config_path, encoding="utf-8") as env_file:
            env_data = yaml.safe_load(env_file)  # 锚点/别名自动展开
        # 替换环境变量
        env_data = self._replace_env_vars(env_data)

        return env_data

    def _clear_cache(self):
        """清除缓存"""
        self.env_config_read.cache_clear()
        self.logger.log_info("清除配置缓存")

    def _replace_env_vars(self, obj):
        """递归替换配置中的环境变量占位符"""
        if isinstance(obj, str):
            # 处理 ${ENV:VAR_NAME:default_value} 格式
            import re

            # 匹配 ${ENV:VAR_NAME:default_value} 格式
            pattern = r"\$\{ENV:([^}]+)\}"
            # 查找所有匹配项
            matches = re.findall(pattern, obj)
            for match in matches:
                parts = match.split(":", 1)
                var_name = parts[0]
                default_value = parts[1] if len(parts) > 1 else ""
                env_value = os.environ.get(var_name, default_value)
                obj = obj.replace(f"${{ENV:{match}}}", env_value)
            return obj
        elif isinstance(obj, dict):
            return {k: self._replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_env_vars(item) for item in obj]
        else:
            return obj

    # ————————外部接口
    def get_current_env(self):
        """获取当前环境名称"""
        config = self.env_config_read()
        return config.get("environment", {}).get("current", "test")

    def get_env_config(self):
        """获取当前环境的配置"""
        config = self.env_config_read()
        current_env = self.get_current_env()
        self.logger.log_info(f"当前环境: {current_env}")
        return config.get("environment", {}).get(current_env, {})

    def get_db_config(self):
        """获取当前环境的数据库配置"""
        config = self.env_config_read
        current_env = self.get_current_env()
        # self.logger.log_info(f"当前数据库配置: {current_env}")
        return config.get("database", {}).get(current_env, {})

    def get_log_config(self):
        """获取当前环境的日志配置"""
        config = self.env_config_read()
        # self.logger.log_info(f"当前日志配置: {current_env}")
        return config.get("logging", {})

    def get_allure_config(self):
        """获取当前环境的allure配置"""
        config = self.env_config_read()
        # self.logger.log_info(f"当前allure配置: {current_env}")
        return config.get("allure", {})

    def get_test_settings(self):
        """获取当前环境的测试配置"""
        config = self.env_config_read()
        # self.logger.log_info(f"当前测试配置: {current_env}")
        return config.get("test_settings", {})

    def get_auth_config(self):
        """获取当前环境的认证配置"""
        config = self.env_config_read()
        # self.logger.log_info(f"当前认证配置: {current_env}")
        return config.get("auth", {})


if __name__ == "__main__":
    yr = ConfigReader()
    # config_info = yr.get_config_info("host")
    # print(config_info)
