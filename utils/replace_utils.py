# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: replace_utils.py
# @Author: Wakka
# @Date: 2025/07/29 16:04
# @Desc: 通用工具函数

import os
import re


def replace_variables(obj, env_vars=None, custom_vars=None):
    """递归替换对象中的环境变量和自定义变量

    Args:
        obj: 要替换的对象，支持字符串、字典、列表
        env_vars: 环境变量字典，默认使用os.environ
        custom_vars: 自定义变量字典

    Returns:
        替换后的对象
    """
    if isinstance(obj, str):
        result = obj

        # 替换自定义变量 {{VAR_NAME}} 格式
        if custom_vars:
            for var_name, var_value in custom_vars.items():
                result = result.replace(f"{{{{{var_name}}}}}", str(var_value))

        # 替换环境变量 {{ENV_VAR}} 格式
        if env_vars is None:
            env_vars = os.environ

        for var_name, var_value in env_vars.items():
            result = result.replace(f"{{{{{var_name}}}}}", str(var_value))

        # 替换 ${ENV:VAR_NAME:default_value} 格式
        pattern = r"\$\{ENV:([^}]+)\}"
        matches = re.findall(pattern, result)
        for match in matches:
            parts = match.split(":", 1)
            var_name = parts[0]
            default_value = parts[1] if len(parts) > 1 else ""
            env_value = env_vars.get(var_name, default_value)
            result = result.replace(f"${{ENV:{match}}}", str(env_value))

        return result

    elif isinstance(obj, dict):
        return {k: replace_variables(v, env_vars, custom_vars) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_variables(item, env_vars, custom_vars) for item in obj]
    else:
        return obj


if __name__ == "__main__":
    from .config_reader_utils import env_config_read

    config = env_config_read("testData/api_config.yaml")
    config = replace_variables(config)
    print(config)
