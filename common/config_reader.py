# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: config_reader.py
# @Author: Wakka
# @Date: 2025/07/23 20:11
# @Desc: 读取项目配置文件，支持环境变量替换

from functools import lru_cache

import yaml
from path_tools import get_project_path, sep


class ConfigReader:
    def __init__(self):
        self.project_path = get_project_path()

    @lru_cache(maxsize=1)
    def env_config_read(self) -> dict:
        """读取项目环境变量, 并缓存结果"""
        config_path = self.project_path + sep(
            ["config", "config.yaml"], add_sep_before=True
        )

        with open(config_path, encoding="utf-8") as env_file:
            env_data = yaml.safe_load(env_file)  # 锚点/别名自动展开
        return env_data

    # ————————外部接口
    def get_config_info(self, key: str):
        """获取配置信息"""
        config_info = self.env_config_read()[key]
        return config_info


if __name__ == "__main__":
    yr = ConfigReader()
    config_info = yr.get_config_info("host")
    print(config_info)
