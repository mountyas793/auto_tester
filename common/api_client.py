# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: api_client.py
# @Author: Wakka
# @Date: 2025/07/23 11:15
# @Desc: 增强版API客户端 - 集成完整日志功能

import json
import logging
import os
from typing import Dict, Any, Optional

from common.read_yaml import get_case
from common.run_method import RequestAdapter

# 配置日志输出到控制台和文件
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 创建logs目录
os.makedirs('logs', exist_ok=True)

# 配置根日志器
logging.basicConfig(
    level=getattr(logging, log_level),
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/api_client.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


class ApiClient:
    """统一的API客户端类 - 增强版"""

    def __init__(self, api_name: str, scenario: str = "success", **kwargs):
        """
        初始化API客户端

        :param api_name: API名称
        :param scenario: 场景名称，默认为success
        :param kwargs: 额外参数，支持动态配置
        """
        self.api_name = api_name
        self.scenario = scenario
        self.config = kwargs
        
        try:
            self.case_spec = get_case(api_name, scenario)
            self.request_adapter = RequestAdapter()
            logger.info(f"初始化ApiClient: {api_name}.{scenario}")
        except Exception as e:
            logger.error(f"初始化ApiClient失败: {api_name}.{scenario} - {str(e)}")
            raise

    def send_request(self, **override_params) -> Dict[str, Any]:
        """
        发送请求并返回结果
        
        :param override_params: 覆盖用例规范的参数
        :return: 响应结果
        """
        try:
            # 合并覆盖参数
            case_spec = {**self.case_spec, **override_params}
            
            logger.info(f"开始发送请求: {self.api_name}.{self.scenario}")
            result = self.request_adapter.send(case_spec)
            
            logger.info(f"请求成功: {self.api_name}.{self.scenario}")
            return result
            
        except Exception as e:
            logger.error(f"请求失败: {self.api_name}.{self.scenario} - {str(e)}")
            raise

    def _build_case_spec(self, api_name: str, scenario: Optional[str] = None) -> dict:
        """
        构建用例规范（兼容旧接口）

        :param api_name: API名称
        :param scenario: 场景名称，可选，默认使用实例配置
        :return: 用例规范字典
        """
        scenario = scenario or self.scenario
        return get_case(api_name, scenario)

    def get_case_info(self) -> Dict[str, Any]:
        """获取当前用例信息"""
        return {
            'api_name': self.api_name,
            'scenario': self.scenario,
            'case_spec': self.case_spec
        }


# 使用示例
if __name__ == "__main__":
    import dotenv
    
    # 加载环境变量
    dotenv.load_dotenv("config/.env")
    
    try:
        # 示例1：基本使用
        api = ApiClient("selectCrmCluePage", "success")
        result = api.send_request()
        
        print(f"状态码: {result.get('code')}")
        print(f"消息: {result.get('msg')}")
        
        # 示例2：动态参数覆盖
        api2 = ApiClient("selectCrmCluePage", "success")
        result2 = api2.send_request(data={"pageNum": 2, "pageSize": 5})
        
        print(f"第二页结果数: {len(result2.get('data', {}).get('list', []))}")
        
    except Exception as e:
        logger.error(f"测试执行失败: {str(e)}")
