# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: db_client.py
# @Author: Wakka
# @Date: 2025/07/24 15:17
# @Desc: 数据库客户端，用于连接数据库、执行 SQL 语句、获取结果等。

import pymysql
from .common_logger import CommonLogger
from .config_reader import ConfigReader


class DbClient:
    def __init__(self):
        """初始化数据库连接"""
        self.logger = CommonLogger()
        self.db_config = ConfigReader().get_config_info("mysql")
        self.host = self.db_config["host"]
        self.port = self.db_config["port"]
        self.user = self.db_config["user"]
        self.password = self.db_config["password"]
        self.db = self.db_config["database"]
        self.conn = None
        self.cursor = None

    def __conn_db(self):
        """连接数据库"""
        try:
            self.logger.log_info(f"正在连接数据库: {self.host}:{self.port}")
            self.conn = pymysql.connect(
                host=str(self.host),
                port=int(self.port),
                user=str(self.user),
                password=str(self.password),
                database=str(self.db),
                charset="utf8mb4",
                connect_timeout=10,  # 连接超时时间设置为10秒
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            self.logger.log_info(f"✅ 数据库连接成功: {self.host}:{self.port}")
            return True
        except pymysql.Error as e:
            self.logger.log_error(f"❌ 数据库连接失败: {e}")
            self.logger.log_error(
                f"配置信息: host={self.host}, port={self.port}, user={self.user}, database={self.db}"
            )
            self.conn = None  # 确保连接失败时conn为None
            self.cursor = None  # 确保cursor为None
            return False

    def __close_conn(self):
        """关闭数据库连接"""
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
        return True

    def __rollback(self):
        """回滚数据库事务"""
        if self.conn is not None:
            self.conn.rollback()
        return True

    def __commit(self):
        """提交数据库事务"""
        if self.conn is not None:
            self.conn.commit()
        return True

    def query(self, sql: str) -> list:
        """查询数据库"""
        self.logger.log_info(f"查询数据库: {sql}")
        query_data = None

        if not self.__conn_db():  # 连接失败直接返回
            self.logger.log_error("❌ 数据库连接失败，无法查询数据")
            return None

        try:
            self.cursor.execute(sql)  # 操作数据库查询
            query_data = self.cursor.fetchall()
            self.logger.log_info("✅ 数据查询成功")
            return query_data
        except pymysql.Error as e:
            self.logger.log_error(f"❌ 数据查询失败: {e}")
            self.__rollback()  # 回滚
            return None
        finally:
            self.__close_conn()  # 关闭数据库连接

    def insert_update_table(self, sql):
        """插入数据或者修改数据"""

        if not self.__conn_db():  # 连接失败直接返回
            self.logger.log_error("❌ 数据库连接失败，无法插入/修改数据")
            return False

        try:
            self.cursor.execute(sql)  # 执行sql
            self.__commit()  # commit一下
            self.logger.log_info("✅ 数据插入/修改成功")
            return True
        except pymysql.Error as e:
            self.logger.log_error(f"❌ 数据插入/修改失败: {e}")
            self.__rollback()  # 回滚
            return False
        finally:
            self.__close_conn()  # 关闭数据库连接


if __name__ == "__main__":
    db_client = DbClient()
    query_data = db_client.query(
        "SELECT * FROM `dc_oa_plus`.`crm_consumer` WHERE `contacts` LIKE '%熊%' LIMIT 0,1000"
    )
    print(query_data)
