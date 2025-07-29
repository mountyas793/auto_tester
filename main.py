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
    from common.config_reader import ConfigReader

    http_config = ConfigReader("config.yaml", env_path="base.config").get_env_config()

    config_reader = ConfigReader("api_config.yaml", env_path="base.test_data")
    print("当前环境:", config_reader.env_config_read(http_config=http_config))
