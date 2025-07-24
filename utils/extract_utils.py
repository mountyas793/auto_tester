# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: extract_utiles.py
# @Author: Wakka
# @Date: 2025/07/23 21:37
# @Desc: 提取器，用于从响应中提取数据
import jsonpath as jsp


def extract(resp, attr_name, exp):
    """
    从响应中提取数据
    :param resp: 响应对象
    :param attr_name: 属性名
    :param exp: 表达式
    :return: 提取到的数据
    """
    try:
        resp_json = resp.json()
    except Exception:
        resp_json = {}

    if attr_name == "json":
        target = resp_json
    else:
        target = resp_json.get(attr_name, {})

    try:
        res = jsp.jsonpath(target, exp)
        if res:
            return res[0]
    except Exception:
        pass
    return None


if __name__ == "__main__":
    import dotenv
    from .common.http_client import HttpClient

    dotenv.load_dotenv("config/.env")

    case_spec = {
        "method": "POST",
        "url": "https://www.cndachang.top/prod-api/dc-project/crmcustom/selectCrmCluePage",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxNTc1NzE1NzY2NzgyOTk2NDgyIiwicm5TdHIiOiJzeU5iRzlFSTZqY3BGbDJlcnpwTldKSDZiRjhvS1drNSIsIm1vYmlsZSI6IjE1MDk4MDEwNzA2In0.2tD5C1kF1YSupOHeD5q1wlT4yGbUPcVULDjRzHFtxLM",
        },
        "body": {"pageNum": 1, "pageSize": 10, "translate": 0},
    }
    session = HttpClient()
    resp = session.send_request(**case_spec)
    # try:
    #     if resp.status_code == 200:
    #         try:
    #             print(resp.json())
    #         except ValueError:
    #             print("响应不是有效的JSON格式:")
    #             print(resp.text)
    #     else:
    #         print(f"请求失败，状态码: {resp.status_code}")
    #         print(resp.text)
    # except Exception as e:
    #     print(f"发生错误: {e}")
    print(extract(resp, "json", "$.data.count"))
