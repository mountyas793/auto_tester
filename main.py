# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: main.py
# @Author: Wakka
# @Date: 2025/07/03 09:57
# @Desc: ...

import dotenv

dotenv.load_dotenv("config/.env")


# 生成测试报告
if __name__ == "__main__":
    # os.system("pytest -s -v testCases/ --alluredir=report/allure-results")
    # os.system("allure generate  report -o report/allure-results")
    # os.system("allure open report/allure-results")
    from common import ConfigReader

    config_reader = ConfigReader()
    print("当前环境:", config_reader.get_env_config())
    print("当前环境的数据库配置:", config_reader.get_db_config())
    print(
        "当前环境的日志配置:",
        config_reader.get_log_config(),
    )
    # db_client = DbClient()
    # query_data = db_client.query(
    #     "SELECT * FROM `dc_oa_plus`.`crm_consumer` WHERE `contacts` LIKE '%熊%' LIMIT 0,1000"
    # )
    # print(query_data)
