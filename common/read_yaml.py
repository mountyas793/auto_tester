# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: read_yaml.py
# @Author: Wakka
# @Date: 2025/07/23 15:34
# @Desc: 读取yaml文件
"""
读取yaml文件
"""

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


def get_case(api_name: str, scenario: str) -> dict:
    """
    返回可直接发请求的 dict，包含：
    url, method, headers, data, expected ...
    """
    data = _load_yaml()  # 缓存读取
    api_cfg = data[api_name]
    base = api_cfg["base"]
    case_cfg = api_cfg["cases"][scenario]

    # 合并：case 覆盖 base
    merged = {**base, **case_cfg}
    merged = _replace_env(merged)  # 替换 {{HOST}} 等

    # 组装完整 URL
    merged["url"] = (
        f"{merged.get('url', '')}{merged['base_url']}{merged['group']}{merged['api']}"
    )
    return merged


if __name__ == "__main__":
    import json

    import dotenv

    dotenv.load_dotenv("config/.env")

    case = get_case("selectCrmCluePage", "success")
    print(json.dumps(case, indent=2))
