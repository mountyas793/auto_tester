# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: read_yaml_copy.py
# @Author: Wakka
# @Date: 2025/07/22 18:02
# @Desc: ...
"""
read_yaml.py  ——  统一读取并合并 API 规格
"""

import os
from copy import deepcopy
from typing import Any, Dict

import yaml


class YamlReader:
    _cache: Dict[str, Dict[str, Any]] = {}  # 文件级缓存

    def __init__(self, yaml_file: str = "testData/api_config.yaml"):
        self.yaml_file = yaml_file

    # ---------- 私有工具 ----------
    def _load_with_cache(self) -> Dict[str, Any]:
        """读取并缓存整个 YAML"""
        if self.yaml_file not in self._cache:
            with open(self.yaml_file, encoding="utf-8") as f:
                self._cache[self.yaml_file] = yaml.safe_load(f)
        return self._cache[self.yaml_file]

    def _replace_placeholders(self, obj: Any) -> Any:
        """递归替换 {{ENV}} 占位符"""
        if isinstance(obj, str):
            for k, v in os.environ.items():
                obj = obj.replace(f"{{{k}}}", v)  # 形如 {{HOST}}
            return obj
        if isinstance(obj, dict):
            return {k: self._replace_placeholders(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._replace_placeholders(item) for item in obj]
        return obj

    # ---------- 校验 ----------
    def _validate_api_config(self, api_name: str, cfg: Dict[str, Any]) -> None:
        if not isinstance(cfg, dict):
            raise ValueError(f"API {api_name} 必须是 dict")
        # base 校验
        base = cfg.get("base", {})
        for field in ("group", "method", "api", "headers"):
            if field not in base:
                raise ValueError(f"API {api_name} 的 base 缺少 {field}")
        # cases 校验
        cases = cfg.get("cases", {})
        if not isinstance(cases, dict):
            raise ValueError(f"API {api_name} 的 cases 必须是 dict")
        for case_name, case in cases.items():
            if "expected" not in case:
                raise ValueError(f"用例 {api_name}.{case_name} 缺少 expected")

    # ---------- 对外唯一接口 ----------
    def get_api_spec(self, api_name: str) -> Dict[str, Any]:
        """
        返回一个 dict：
        {
            "base": {...公共字段...},
            "cases": {
                "success": { url, method, headers, data, expected, ... },
                "invalid_id": { ... },
                ...
            }
        }
        每个 case 都已合并 base，可直接发请求。
        """
        raw = self._load_with_cache()
        if api_name not in raw:
            raise ValueError(f"API {api_name} 不存在")
        api_cfg = deepcopy(raw[api_name])
        # print(api_cfg)
        self._validate_api_config(api_name, api_cfg)

        # 1. 替换占位符
        api_cfg = self._replace_placeholders(api_cfg)

        base = api_cfg["base"]
        cases = api_cfg["cases"]

        # 2. 把 base 合并到每个 case，形成完整 spec
        merged_cases = {}
        for case_name, case in cases.items():
            full_case = deepcopy(base)  # 先拷贝 base
            full_case.update(case)  # 用例层覆盖
            merged_cases[case_name] = full_case

        return {"base": base, "cases": merged_cases}


# -------------- DEMO --------------
if __name__ == "__main__":
    import json

    from dotenv import load_dotenv

    load_dotenv("config/.env")

    reader = YamlReader("testData/api_config.yaml")
    spec = reader.get_api_spec("AddMaterialCategory")
    print(json.dumps(spec, ensure_ascii=False, indent=2))
