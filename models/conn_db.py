import pymysql
import config
import pandas as pd
from utils.logger import logger
from DBUtils.PooledDB import PooledDB


class ConnDBPool(object):
    __pool = None

    def __init__(self):
        self.__pool = PooledDB(**config.mysql_connect_pool_options)

    def register_connect(self):
        _conn = self.__pool.connection()
        _cursor = _conn.cursor(cursor=pymysql.cursors.DictCursor)
        return _conn, _cursor

    @staticmethod
    def logout_connect(_conn, _cursor):
        """关闭数据库连接"""
        try:
            _cursor.close()
            _conn.close()
        except pymysql.MySQLError as e:
            logger.info("放回数据库连接池失败。")

    def get_dict(self, sql):
        _conn, _cursor = self.register_connect()
        query_dict_res = ''
        try:
            # 执行sql语句
            _cursor.execute(sql)
            query_dict_res = _cursor.fetchall()
        except Exception as e:
            logger.error('发生异常:', e)
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
            logger.error('发生异常:', e)
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
            logger.error('发生异常:', e)
            # 发生错误时回滚
            _conn.rollback()
        self.logout_connect(_conn, _cursor)
        return execute_res


conn_pool = ConnDBPool()


if __name__ == '__main__':
    sql_query = """
                    select count(1) from third_xinfangjian
                """
    logger.info(conn_pool.get_dict(sql_query))