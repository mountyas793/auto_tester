# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: run_method.py
# @Author: Wakka
# @Date: 2025/07/23 09:57
# @Desc: 运行方法 - 完整的请求适配器

import json
import time
from typing import Any, Dict, Optional

import requests

from common.api_logs import HTTPRequestLogger


class RequestAdapter:
    """requests适配器"""

    def __init__(self):
        """
        初始化请求适配器
        """
        self.logger = HTTPRequestLogger("request_adapter", json_format=True)

    def send(self, case_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送请求并记录详细日志

        :param case_spec: 用例规范
        :return: 响应结果
        """
        # 记录请求开始时间
        start_time = time.time()

        try:
            # 参数验证
            required_fields = ["url", "method"]
            for field in required_fields:
                if field not in case_spec:
                    raise ValueError(f"缺少必需字段: {field}")

            # 构建请求参数
            request_params = {
                "url": case_spec["url"],
                "method": case_spec["method"].upper(),
                "headers": case_spec.get("headers", {}),
            }

            # 添加请求数据
            if "data" in case_spec and case_spec["data"]:
                if (
                    request_params["headers"].get("Content-Type", "").lower()
                    == "application/x-www-form-urlencoded"
                ):
                    request_params["data"] = case_spec["data"]
                else:
                    request_params["json"] = case_spec["data"]

            # 添加查询参数
            if "params" in case_spec and case_spec["params"]:
                request_params["params"] = case_spec["params"]

            self.logger.logger.info(
                f"准备发送请求: {case_spec['method'].upper()} - {case_spec['url']}"
            )

            # 发送请求
            response = requests.request(**request_params)

            # 记录完整HTTP事务
            self.logger.log_full_http_transaction(response)

            # 计算耗时
            elapsed = time.time() - start_time

            # 验证响应
            response.raise_for_status()

            # 解析JSON响应
            try:
                result = response.json()
                self.logger.logger.info(f"请求完成，耗时: {elapsed:.2f}s")
                return result
            except json.JSONDecodeError as e:
                self.logger.logger.error(f"响应JSON解析失败: {str(e)}")
                raise

        except requests.exceptions.RequestException as e:
            elapsed = time.time() - start_time
            self.logger.logger.error(f"请求异常，耗时: {elapsed:.2f}s - {str(e)}")
            raise
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.logger.error(f"处理异常，耗时: {elapsed:.2f}s - {str(e)}")
            raise

    def validate_response(
        self, response: Dict[str, Any], expected: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        验证响应结果

        :param response: 响应数据
        :param expected: 预期结果
        :return: 是否验证通过
        """
        if not expected:
            return True

        for key, expected_value in expected.items():
            if key not in response:
                self.logger.logger.warning(f"响应缺少预期字段: {key}")
                return False

            if response[key] != expected_value:
                self.logger.logger.warning(
                    f"字段验证失败: {key}={response[key]} (期望: {expected_value})"
                )
                return False

        return True


if __name__ == "__main__":
    import json

    import dotenv

    # 加载环境变量
    dotenv.load_dotenv("config/.env")

    from common.read_yaml import get_case

    try:
        spec = get_case("selectCrmCluePage", "success")
        adapter = RequestAdapter()

        print("🚀 开始执行测试...")
        resp = adapter.send(spec)

        print("✅ 测试执行成功")
        print(f"📊 响应状态: {resp.get('code')}")
        print(f"📋 消息: {resp.get('msg')}")

        # 验证响应
        expected = spec.get("expected", {})
        is_valid = adapter.validate_response(resp, expected)
        print(f"🔍 验证结果: {'通过' if is_valid else '失败'}")

    except Exception as e:
        print(f"❌ 测试执行失败: {str(e)}")
