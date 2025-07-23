# api_logs.py  （保持无耦合，只改日志器）
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Dict


class RequestLogger:
    """单例 Request 日志器"""

    _instance = None

    def __new__(cls, log_dir="logs", log_name="requests", backup_days=7, console=True):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup(log_dir, log_name, backup_days, console)
        return cls._instance

    # ---------- 内部 ----------
    def _setup(self, log_dir, log_name, backup_days, console):
        self.logger = logging.getLogger("HttpLogger")
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
        self, method: str, url: str, headers: Dict[str, Any], body: Any = None
    ):
        self.logger.info(
            ">>> %s请求%s\n%s %s\nHeaders: %s\nBody: %s",
            "".join(["- " for _ in range(10)]),
            "".join(["- " for _ in range(10)]),
            method,
            url,
            json.dumps(headers, ensure_ascii=False),
            json.dumps(body, ensure_ascii=False),
        )

    def log_response(self, status: int, headers: Dict[str, Any], message: Any):
        self.logger.info(
            "<<< %s响应%s\nStatus: %s\nHeaders: %s\nBody: %s",
            "".join(["- " for _ in range(10)]),
            "".join(["- " for _ in range(10)]),
            status,
            json.dumps(headers, ensure_ascii=False),
            json.dumps(message, ensure_ascii=False)
            if isinstance(message, (dict, list))
            else str(message),
        )
