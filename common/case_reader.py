# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: case_reader.py
# @Author: Wakka
# @Date: 2025/07/24 14:24
# @Desc: 读取测试用例yaml文件，替换环境变量，返回字典
import os
from functools import lru_cache

import yaml


@lru_cache(maxsize=1)
def _load_yaml(path: str = "testData/api_config.yaml") -> dict:
    """只读一次，缓存结果"""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)  # 锚点/别名自动展开


def _replace_env(obj):
    """递归替换 {{ENV}}"""
    if isinstance(obj, str):
        for k, v in os.environ.items():
            obj = obj.replace(f"{{{{{k}}}}}", v)
        return obj
    if isinstance(obj, dict):
        return {k: _replace_env(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_replace_env(i) for i in obj]
    return obj


def case_read(path: str = "testData/api_config.yaml") -> dict:
    """读取yaml文件, 替换环境变量, 返回字典"""
    data = _load_yaml(path)
    return _replace_env(data)


if __name__ == "__main__":
    data = case_read()
    print(data)
