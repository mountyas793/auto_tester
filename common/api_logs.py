# logger.py  —— 只负责记录
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Dict

from requests import Response


class HttpLogger:
    """HTTP 日志器"""

    _instance = None  # 单例，防止重复创建 logger

    def __new__(cls, log_dir="logs", log_name="requests", backup_days=7, console=True):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup(log_dir, log_name, backup_days, console)
        return cls._instance

    # ---------- 内部 ----------
    def _setup(self, log_dir, log_name, backup_days, console):
        self.logger = logging.getLogger("HttpLogger")
        if self.logger.handlers:  # 已配置过
            return

        self.logger.setLevel(logging.INFO)
        fmt = "%(asctime)s [%(levelname)s] %(message)s"
        formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

        if console:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        os.makedirs(log_dir, exist_ok=True)
        fh = TimedRotatingFileHandler(
            filename=os.path.join(log_dir, f"{log_name}.log"),
            when="midnight",
            interval=1,
            backupCount=backup_days,
            encoding="utf-8",
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    # ---------- 供外部调用的唯一方法 ----------
    def log_round_trip(self, case_spec: Dict[str, Any], response: Response):
        """记录一次完整的请求+响应"""
        self.logger.info("=" * 50)
        # 记录请求
        self.logger.info(
            ">>> %s请求%s\n%s %s\nHeaders: %s\nBody: %s",
            "- " * 5,
            "- " * 5,
            case_spec["method"],
            case_spec["url"],
            json.dumps(case_spec.get("headers", {}), ensure_ascii=False),
            json.dumps(case_spec.get("body", {}), ensure_ascii=False),
        )

        self.logger.info("=" * 50)
        # 记录响应
        self.logger.info(
            "<<< %s响应%s\nStatus: %s\nHeaders: %s\nBody: %s",
            "- " * 5,
            "- " * 5,
            response.status_code,
            json.dumps(response.headers or {}, ensure_ascii=False),
            json.dumps(response.json(), ensure_ascii=False)
            if isinstance(response.json(), (dict, list))
            else str(response.json()),
        )


if __name__ == "__main__":
    import requests

    logger = HttpLogger()
    case_spec = {
        "name": "获取用户信息",
        "method": "GET",
        "url": "https://www.baidu.com",
        "headers": {"User-Agent": "Python/3.11"},
    }
    response = requests.get(case_spec["url"], headers=case_spec["headers"])
    logger.log_round_trip(case_spec, response)
    print(response.json())
