## 项目概述

这是一个基于 Python 的自动化测试框架，采用分层架构设计，支持 API 接口测试、数据库操作和测试报告生成。

## 技术栈

- 核心语言 : Python 3.11+
- 测试框架 : pytest + allure-pytest
- HTTP 客户端 : requests
- 数据库 : pymysql (MySQL)
- 配置管理 : YAML + python-dotenv
- 日志系统 : 自定义单例日志器
- 路径管理 : pathlib
- 数据提取 : jsonpath

## 架构分层

### 1. 配置管理层

- ConfigReader ( common/config_reader.py ): 读取 YAML 配置文件，支持环境变量替换
- PathManager ( common/path_manager.py ): 统一路径管理，自动解析变量引用
- 配置文件 :
  - config/config.yaml : 环境配置、数据库配置、API 认证、测试设置
  - config/paths.yaml : 项目路径配置
  - .env : 环境变量文件

### 2. 数据访问层

- HttpClient ( common/http_client.py ): HTTP 请求封装，支持日志记录
- DbClient ( common/db_client.py ): 数据库操作封装，支持 MySQL 连接

### 3. 业务逻辑层

- RunnerUtils ( utils/runner_utils.py ): 测试执行引擎，支持 request/response/extract 操作
- ExtractUtils ( utils/extract_utils.py ): JSON 数据提取工具
- ReplaceUtils ( utils/replace_utils.py ): 变量替换工具

### 4. 测试用例层

- 测试数据 : testData/api_config.yaml - 定义测试用例数据
- 测试脚本 : testCases/test_demo.py - pytest 测试用例
- CaseReader ( common/case_reader.py ): 测试用例读取器

### 5. 报告生成层

- AllureBuilder ( common/allure_builder.py ): Allure 报告构建器
- 日志系统 : common/common_logger.py - 单例日志器

## 运行流程

### 测试执行流程

1. 1. 环境初始化 : pytest 加载 pytest.ini 配置
2. 2. 测试发现 : 自动发现 testCases 目录下的测试文件
3. 3. 用例执行 :
   - 读取测试数据 (CaseReader)
   - 替换环境变量 (ReplaceUtils)
   - 执行 HTTP 请求 (HttpClient)
   - 验证响应结果 (RunnerUtils)
   - 提取关键数据 (ExtractUtils)
4. 4. 报告生成 : Allure 报告 + 日志文件

### 配置加载流程

1. 1. 路径解析 : PathManager 解析所有路径
2. 2. 配置读取 : ConfigReader 加载环境配置
3. 3. 变量替换 : ReplaceUtils 处理环境变量
4. 4. 参数传递 : 将配置传递给各模块使用

## 目录结构

```
auto_tester/
├── common/                 # 公共模块
│   ├── config_reader.py   # 配置读取器
│   ├── path_manager.py    # 路径管理器
│   ├── http_client.py     # HTTP客户端
│   ├── db_client.py       # 数据库客户端
│   ├── common_logger.py   # 日志管理器
│   ├── case_reader.py     # 用例读取器
│   └── allure_builder.py  # 报告构建器
├── config/                # 配置文件
│   ├── config.yaml       # 主配置
│   └── paths.yaml        # 路径配置
├── testCases/            # 测试用例
│   └── test_demo.py      # 测试脚本
├── testData/             # 测试数据
│   └── api_config.yaml   # 测试用例数据
├── utils/                # 工具函数
│   ├── runner_utils.py   # 测试运行器
│   ├── extract_utils.py  # 数据提取工具
│   └── replace_utils.py  # 变量替换工具
├── logs/                 # 日志目录
├── report/               # 测试报告
├── .venv/                # 虚拟环境
├── main.py               # 主入口
├── pyproject.toml        # 项目配置
└── pytest.ini           # pytest配置
```

## 核心特性

- 环境隔离 : 支持 test/prod 环境切换
- 配置管理 : YAML 配置 + 环境变量
- 日志追踪 : 完整的请求响应日志
- 数据驱动 : YAML 格式测试数据
- 报告丰富 : Allure 可视化报告
- 扩展性强 : 模块化设计，易于扩展

## 使用方式

1. 1. 安装依赖 : uv sync
2. 2. 运行测试 : uv run pytest testCases/test_demo.py -v
3. 3. 生成报告 : uv run pytest --alluredir=report/allure-results
4. 4. 查看报告 : allure serve report/allure-results
