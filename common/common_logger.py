# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: common_logger.py
# @Author: Wakka
# @Date: 2025/07/24 13:48
# @Desc: 通用日志器，用于记录系统运行日志、错误日志等。


import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Dict


class CommonLogger:
    """单例 通用日志器"""

    # 单例实例
    _instance = None

    def __new__(cls, log_dir="logs", log_name="requests", backup_days=7, console=True):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup(log_dir, log_name, backup_days, console)
        return cls._instance

    # ---------- 内部 ----------
    def _setup(self, log_dir, log_name, backup_days, console):
        """初始化日志器"""
        self.logger = logging.getLogger("CommonLogger")
        if self.logger.handlers:
            return

        self.logger.setLevel(logging.INFO)
        fmt = "%(asctime)s [%(levelname)s] %(message)s"
        formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

        # 控制台输出
        if console:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        os.makedirs(log_dir, exist_ok=True)
        fh = TimedRotatingFileHandler(
            os.path.join(log_dir, f"{log_name}.log"),
            when="midnight",
            interval=1,
            backupCount=backup_days,
            encoding="utf-8",
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    # ---------- 对外 ----------
    def log_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, Any],
        body: Any = None,
        level=logging.INFO,
    ):
        """记录HTTP请求"""
        message = {
            "type": "request",
            "method": method,
            "url": url,
            "headers": headers,
            "body": body,
        }
        self.logger.info(
            ">>> %s请求%s\n%s\n%s\n%s",
            "".join(["- " for _ in range(10)]),
            "".join(["- " for _ in range(10)]),
            f"> 方法&URL: {message['method']} - {message['url']}",
            f"> 头信息: {json.dumps(message['headers'], ensure_ascii=False)}",
            f"> 请求体: {json.dumps(message['body'], ensure_ascii=False)}"
            if isinstance(message["body"], (dict, list))
            else f"> 请求体: {message['body']}",
        )

    def log_response(
        self, status: int, headers: Dict[str, Any], message: Any, level=logging.INFO
    ):
        """记录HTTP响应"""
        response_data = {
            "type": "response",
            "status": status,
            "headers": headers,
            "body": message,
        }
        self.logger.info(
            "<<< %s响应%s\n%s\n%s\n%s",
            "".join(["- " for _ in range(10)]),
            "".join(["- " for _ in range(10)]),
            f"> 状态码: {response_data['status']}",
            f"> 响应头: {json.dumps(response_data['headers'], ensure_ascii=False)}",
            f"> 响应体: {json.dumps(response_data['body'], ensure_ascii=False)}"
            if isinstance(response_data["body"], (dict, list))
            else f"> 响应体: {response_data['body']}",
        )

    def log_debug(self, msg: str):
        self.logger.debug(msg)

    def log_info(self, msg: str):
        self.logger.info(msg)

    def log_warning(self, msg: str):
        self.logger.warning(msg)

    def log_error(self, msg: str):
        self.logger.error(msg)

    def log_critical(self, msg: str):
        self.logger.critical(msg)
