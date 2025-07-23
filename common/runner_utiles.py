# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: runner_utiles.py
# @Author: Wakka
# @Date: 2025/07/23 21:30
# @Desc: ...
import requests_validator as validator

from common.extract_utiles import extract
from common.logger import RequestLogger
from common.run_method import HttpSession


def runner(k, v, var):
    """
    运行器
    :param k: 关键字
    :param v: 参数
    :param var: 变量
    :return:
    """
    logger = RequestLogger()
    resp = None
    match k:
        case "request":  # 请求
            logger.log_info("1. 开始发送请求……")
            var["resp"] = HttpSession().send(**v)
            resp = var["resp"]
        case "response":  # 响应校验
            logger.log_info("2. 开始校验响应……")
            validator.validate(resp, **v)
        case "extract":  # 提取
            logger.log_info("3. 开始提取变量……")
            for var_name, var_exp in v.items():
                value = extract(resp, *var_exp)
                logger.log_info(f"3.1 提取变量 {var_name} 的值为：{value}")
                var[var_name] = value


if __name__ == "__main__":
    var = {}
    runner("request", {"url": "https://www.baidu.com"}, var)
    runner("response", {"status_code": 200}, var)
    runner("extract", {"content": ["json", "$.content"]}, var)
    print(var)
