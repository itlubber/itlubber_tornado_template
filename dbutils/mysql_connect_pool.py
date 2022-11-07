# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/18 23:42
@Author  : itlubber
@Site    : itlubber.art
"""

import pymysql
import pandas as pd

from .pooled_db import PooledDB


class MysqlConnectPool(object):
    __pool = None

    def __init__(self, **kwargs):
        self.__pool = PooledDB(creator=pymysql, **kwargs)

    def register_connect(self):
        _conn = self.__pool.connection()
        _cursor = _conn.cursor(cursor=pymysql.cursors.DictCursor)
        return _conn, _cursor

    @staticmethod
    def logout_connect(_conn, _cursor):
        try:
            _cursor.close()
            _conn.close()
        except pymysql.MySQLError as e:
            raise "放回数据库连接池失败。"

    def get_dict(self, sql):
        _conn, _cursor = self.register_connect()
        query_dict_res = ''
        try:
            # 执行sql语句
            _cursor.execute(sql)
            query_dict_res = _cursor.fetchall()
        except Exception as e:
            raise f'发生异常: {e}'
        finally:
            self.logout_connect(_conn, _cursor)
        return query_dict_res

    def get_dataframe(self, sql):
        _conn, _cursor = self.register_connect()
        query_dict_res = ''
        try:
            # 执行sql语句
            _cursor.execute(sql)
            query_dict_res = pd.DataFrame(_cursor.fetchall())
        except pymysql.MySQLError as e:
            raise f'发生异常: {e}'
        finally:
            self.logout_connect(_conn, _cursor)
        return query_dict_res

    def execute_sql(self, sql):
        _conn, _cursor = self.register_connect()
        execute_res = False
        try:
            # 执行SQL语句
            _cursor.execute(sql)
            # 提交到数据库执行
            _conn.commit()
            execute_res = True
        except pymysql.MySQLError as e:
            _conn.rollback()
            raise f'发生异常: {e}'
        finally:
            self.logout_connect(_conn, _cursor)
        return execute_res
