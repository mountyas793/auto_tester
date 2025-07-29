# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: runner_utiles.py
# @Author: Wakka
# @Date: 2025/07/23 21:30
# @Desc: 运行器，根据关键字，调用不同的函数，实现不同的功能

from ..common.http_client import HttpClient
from .extract_utils import extract


def runner(k, v, var, log_config=None, env_config=None):
    """
    运行器
    :param k: 关键字
    :param v: 参数
    :param var: 变量
    :return:
    """
    from ..common.common_logger import CommonLogger

    logger = CommonLogger(log_config=log_config, env_config=env_config)
    resp = var.get("resp")
    match k:
        case "request":  # 请求
            logger.log_info("1. 开始发送请求……")
            var["resp"] = HttpClient().send_request(**v)

        case "response":  # 响应校验
            logger.log_info("2. 开始校验响应……")
            if resp is None:
                raise ValueError("没有可用的响应对象，请先执行request步骤")

            resp_json = resp.json()
            assert resp_json["code"] == v["code"]
            assert resp_json["msg"] == v["msg"]

            logger.log_info(
                f"2.1 校验响应状态码为：{resp_json['code']}，响应状态码为：{v['code']}"
            )
            logger.log_info(
                f"2.2 校验响应消息为：{resp_json['msg']}，响应消息为：{v['msg']}"
            )

        case "extract":  # 提取
            logger.log_info("3. 开始提取变量……")
            if resp is None:
                raise ValueError("没有可用的响应对象，请先执行request步骤")
            for var_name, var_exp in v.items():
                value = extract(resp, *var_exp)
                logger.log_info(f"3.1 提取变量 {var_name} 的值为：{value}")
                var[var_name] = value


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv("config/.env")
    from .yaml_utils import _load_yaml, _replace_env

    data = _replace_env(_load_yaml("testData/test_api.yaml")["steps"][0]["request"])
    var = {}
    runner(
        "request",
        data,
        var,
    )
    # print(var["resp"].json()["msg"])
