# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: runner_utiles.py
# @Author: Wakka
# @Date: 2025/07/23 21:30
# @Desc: 运行器，根据关键字，调用不同的函数，实现不同的功能

from extract_utils import extract
from logs_utils import LoggerUtils
from requests_utils import RequestsUtils


def runner(k, v, var):
    """
    运行器
    :param k: 关键字
    :param v: 参数
    :param var: 变量
    :return:
    """
    logger = LoggerUtils()
    resp = None
    match k:
        case "request":  # 请求
            logger.log_info("1. 开始发送请求……")
            # print("1. 开始发送请求……")
            var["resp"] = RequestsUtils().send_request(**v)
            resp = var["resp"]
        case "response":  # 响应校验
            logger.log_info("2. 开始校验响应……")
            # print("2. 开始校验响应……")
            assert resp.status_code == v["code"]
            assert resp.json()["msg"] == v["msg"]
        case "extract":  # 提取
            logger.log_info("3. 开始提取变量……")
            # print("3. 开始提取变量……")
            for var_name, var_exp in v.items():
                value = extract(resp, *var_exp)
                logger.log_info(f"3.1 提取变量 {var_name} 的值为：{value}")
                # print(f"3.1 提取变量 {var_name} 的值为：{value}")
                var[var_name] = value


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv("config/.env")
    from yaml_utils import _load_yaml, _replace_env

    data = _replace_env(_load_yaml("testData/test_api.yaml")["steps"][0]["request"])
    var = {}
    runner(
        "request",
        data,
        var,
    )
    # print(var["resp"].json()["msg"])
