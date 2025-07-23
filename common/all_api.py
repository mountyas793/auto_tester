# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: all_api.py
# @Author: Wakka
# @Date: 2025/07/23 11:15
# @Desc: 完整的API测试框架 - 集成日志和高级功能

import json
import logging
import os
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from common.api_client import ApiClient
from common.read_yaml import YamlReader

logger = logging.getLogger(__name__)


class AllApi:
    """完整的API测试框架"""

    def __init__(self, yaml_reader: YamlReader):
        """
        初始化API测试框架
        
        :param yaml_reader: YAML配置读取器
        """
        self.yaml_reader = yaml_reader
        self.clients = {}
        self.results = {}
        
    def get_api_client(self, api_name: str, scenario: str = "success") -> ApiClient:
        """
        获取API客户端实例
        
        :param api_name: API名称
        :param scenario: 场景名称
        :return: API客户端实例
        """
        key = f"{api_name}_{scenario}"
        if key not in self.clients:
            self.clients[key] = ApiClient(api_name, scenario)
        return self.clients[key]

    def execute_single(self, api_name: str, scenario: str = "success", **override_params) -> Dict[str, Any]:
        """
        执行单个API测试
        
        :param api_name: API名称
        :param scenario: 场景名称
        :param override_params: 覆盖参数
        :return: 测试结果
        """
        try:
            client = self.get_api_client(api_name, scenario)
            result = client.send_request(**override_params)
            
            self.results[f"{api_name}_{scenario}"] = {
                'status': 'success',
                'result': result,
                'timestamp': self._get_timestamp()
            }
            
            logger.info(f"✅ 测试执行成功: {api_name}.{scenario}")
            return result
            
        except Exception as e:
            self.results[f"{api_name}_{scenario}"] = {
                'status': 'failed',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
            
            logger.error(f"❌ 测试执行失败: {api_name}.{scenario} - {str(e)}")
            raise

    def execute_batch(self, test_cases: List[Dict[str, Any]], max_workers: int = 3) -> Dict[str, Any]:
        """
        批量执行API测试
        
        :param test_cases: 测试用例列表
        :param max_workers: 最大并发数
        :return: 批量测试结果
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_case = {}
            
            for case in test_cases:
                api_name = case['api_name']
                scenario = case.get('scenario', 'success')
                override_params = case.get('override_params', {})
                
                future = executor.submit(
                    self.execute_single, 
                    api_name, 
                    scenario, 
                    **override_params
                )
                future_to_case[future] = f"{api_name}_{scenario}"
            
            for future in as_completed(future_to_case):
                case_key = future_to_case[future]
                try:
                    result = future.result()
                    results[case_key] = {
                        'status': 'success',
                        'result': result
                    }
                except Exception as e:
                    results[case_key] = {
                        'status': 'failed',
                        'error': str(e)
                    }
        
        return results

    def get_test_summary(self) -> Dict[str, Any]:
        """获取测试执行摘要"""
        total = len(self.results)
        success = sum(1 for r in self.results.values() if r['status'] == 'success')
        failed = total - success
        
        return {
            'total_tests': total,
            'success_count': success,
            'failed_count': failed,
            'success_rate': (success / total * 100) if total > 0 else 0,
            'results': self.results
        }

    def save_results(self, filename: str = None) -> str:
        """
        保存测试结果到文件
        
        :param filename: 文件名，默认为当前时间
        :return: 保存的文件路径
        """
        if not filename:
            filename = f"test_results_{self._get_timestamp()}.json"
        
        filepath = os.path.join('logs', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        summary = self.get_test_summary()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📁 测试结果已保存: {filepath}")
        return filepath

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime('%Y%m%d_%H%M%S')


class AllApiWithLogging(AllApi):
    """带日志的API测试框架（向后兼容）"""
    
    def __init__(self, yaml_reader: YamlReader):
        super().__init__(yaml_reader)
        logger.info("初始化AllApiWithLogging")


# 使用示例
if __name__ == "__main__":
    import dotenv
    
    # 加载环境变量
    dotenv.load_dotenv("config/.env")