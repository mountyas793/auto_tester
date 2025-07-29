# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: path_manager.py
# @Author: Wakka
# @Date: 2025/07/28 14:34
# @Desc: 项目路径管理器，负责加载和解析YAML配置的路径

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml


class PathManager:
    """项目路径管理器，负责加载和解析YAML配置的路径"""

    def __init__(self, config_path: str = "config/paths.yaml"):
        """
        初始化路径管理器
        Args:
            config_path: 路径配置YAML文件的相对路径，相对于项目根目录
        """
        self.config_path = self._resolve_absolute_path(config_path)
        self.path_config = self._load_config()
        self.resolved_paths = self._resolve_paths()

        # 创建所有目录（如果不存在）
        self._create_directories()

    def _resolve_absolute_path(self, relative_path: str) -> Path:
        """解析相对路径为绝对路径（基于项目根目录）"""
        # 从当前文件路径回溯找到项目根目录
        current_dir = Path(__file__).resolve().parent
        root_dir = current_dir
        # 查找项目根目录的标识文件（main.py作为入口文件）
        while not (root_dir / "main.py").exists():
            root_dir = root_dir.parent
            if root_dir == Path("/"):
                raise FileNotFoundError("找不到项目根目录（未发现main.py）")

        return root_dir / relative_path

    @lru_cache(maxsize=1)
    def _load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"路径配置文件不存在: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _resolve_paths(self) -> Dict[str, Path]:
        """解析包含变量的路径"""
        resolved = {}

        # 首先解析基础路径
        base_paths = self.path_config.get("base", {})
        for key, value in base_paths.items():
            resolved[f"base.{key}"] = self._interpolate_path(value, resolved)

        # 解析其他路径组
        for group, paths in self.path_config.items():
            if group == "base":
                continue

            for key, value in paths.items():
                resolved[f"{group}.{key}"] = self._interpolate_path(value, resolved)

        return resolved

    def _interpolate_path(self, path_str: str, resolved_paths: Dict[str, Path]) -> Path:
        """解析包含变量引用的路径字符串"""
        # 替换变量引用（如${base.root}）
        for var_name, var_path in resolved_paths.items():
            path_str = path_str.replace(f"${{{var_name}}}", str(var_path))

        return Path(path_str).resolve()

    def _create_directories(self) -> None:
        """创建所有配置的目录（如果不存在）"""
        for path in self.resolved_paths.values():
            if not path.exists():
                # 检查是否是文件路径，如果是则创建其父目录
                if "." in path.name:  # 简单判断是否为文件
                    path.parent.mkdir(parents=True, exist_ok=True)
                else:  # 目录路径
                    path.mkdir(parents=True, exist_ok=True)

    def get_path(self, path_key: str) -> Path:
        """
        获取指定键对应的路径

        Args:
            path_key: 路径键（如"testData.api_config"）

        Returns:
            解析后的绝对路径
        """
        if path_key not in self.resolved_paths:
            raise KeyError(
                f"路径键不存在: {path_key}，可用键: {list(self.resolved_paths.keys())}"
            )

        return self.resolved_paths[path_key]

    def get_all_paths(self) -> Dict[str, Path]:
        """返回所有解析后的路径字典"""
        return self.resolved_paths.copy()

    def __repr__(self) -> str:
        return f"PathManager(config_path={self.config_path}, paths={list(self.resolved_paths.keys())})"


if __name__ == "__main__":
    # 单例模式的路径管理器实例
    path_manager = PathManager()
    # 示例：获取测试数据目录路径
    test_data_path = path_manager.get_path("base.config")
    print(f"测试数据目录路径: {test_data_path}")
