# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: path_tools.py
# @Author: Wakka
# @Date: 2025/07/24 13:56
# @Desc: 获取项目目录，拼接路径
import os


def get_project_path():
    """获取项目目录"""
    project_name = "auto_tester"  # auto_tester为项目名称
    file_path = os.path.dirname(__file__)  # 获取当前路径
    # print("当前路径:", file_path)
    project_path = file_path[
        : file_path.find(project_name) + len(project_name)
    ]  # 截取项目路径
    return project_path


def sep(path, add_sep_before=False, add_sep_after=False):
    """拼接文件路径，添加系统分隔符"""
    # 拼接传入的数组
    all_path = os.sep.join(path)
    # 如果before为TRUE，那就在路径前面加“/”
    if add_sep_before:
        all_path = os.sep + all_path
    # 如果after为TRUE，那就在路径后面加“/”
    if add_sep_after:
        all_path = all_path + os.sep
    return all_path


if __name__ == "__main__":
    print(get_project_path())
    print(sep(["config", "api_config.yaml"], add_sep_before=True))
