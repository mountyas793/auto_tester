# -*- coding: utf-8 -*-
# @Project: 321_Python
# @File: prepare_logs.py
# @Author: Wakka
# @Date: 2025/07/09 14:00
# @Desc: 封装日志模块
import logging
import os
from typing import Any, Dict, Optional


class PrepareLogs:
    """
    通用的日志工具类
    """

    def __init__(
        self,
        name: str = "requests",
        log_file: str = "logs/requests.log",
        level: int = logging.INFO,
    ) -> None:
        """
        初始化日志配置
        :param name: 日志器名称
        :param log_file: 日志文件路径
        :param level: 日志级别
        """
        # 确保日志目录存在
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 时间格式
        time_format = "%Y-%m-%d %H:%M:%S"

        # 日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s",
            datefmt=time_format,
        )

        # 文件handler
        file_handler = logging.FileHandler(
            filename=log_file, encoding="utf-8", mode="w"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # # 控制台输出
        # console_handler = logging.StreamHandler()
        # console_handler.setFormatter(formatter)
        # self.logger.addHandler(console_handler)

    def log_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        body: Optional[Any] = None,
    ) -> None:
        """
        记录请求日志
        """
        self.logger.info(f"接口地址  ---->>: {method}  {url}")
        # print(f"接口地址  ---->>: {method}  {url}")
        if headers:
            self.logger.info(f"请求头  ---->>: {headers}")
            # print(f"请求头  ---->>: {headers}")
        if body:
            self.logger.info(f"请求体  ---->>: {body}")
            # print(f"请求体  ---->>: {body}")

    def log_response(
        self,
        status_code: int,
        headers: Optional[Dict] = None,
        content: Optional[Any] = None,
    ) -> None:
        """
        记录响应日志
        """
        self.logger.info(f"状态码  <<----: {status_code}")
        # print(f"状态码  <<----: {status_code}")
        if headers:
            self.logger.info(f"响应头  <<----: {headers}")
        if content:
            self.logger.info(f"响应体  <<----: {content}")


def main():
    pass


if __name__ == "__main__":
    main()
