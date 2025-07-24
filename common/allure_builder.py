# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: allure_builder.py
# @Author: Wakka
# @Date: 2025/07/24 14:36
# @Desc: 构建allure报告

import allure


def build_allure_report(data, res):
    """构建allure报告"""
    allure.title(data["name"])

    res_url = str(res.request.url)
    allure.attach(res_url, "请求地址")

    method = str(res.request.method)
    allure.attach(method, "请求方法")

    headers = str(res.request.headers)
    allure.attach(headers, "请求头")

    body = str(data)
    allure.attach(body, "请求体")

    resp_time = str(res.elapsed.total_seconds() * 1000)
    allure.attach(resp_time, "响应时间")

    resp_status_code = str(res.status_code)
    allure.attach(resp_status_code, "响应状态码")

    resp_body = str(res.text)
    allure.attach(resp_body, "响应体")


if __name__ == "__main__":
    from case_reader import case_read
    from config_reader import ConfigReader

    data = case_read()

    host = ConfigReader().get_config_info("host")["dev"]
    url = data["steps"][0]["request"]["url"]
    baseurl = url.replace(str("{{HOST}}"), host)
