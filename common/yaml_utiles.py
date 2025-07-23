# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: yaml_utiles.py
# @Author: Wakka
# @Date: 2025/07/23 20:11
# @Desc: ...


from functools import lru_cache

import yaml


@lru_cache(maxsize=1)
def load_yaml(path: str = "testData/test_api.yaml") -> dict:
    """只读一次，缓存结果"""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)  # 锚点/别名自动展开


if __name__ == "__main__":
    print(load_yaml())
