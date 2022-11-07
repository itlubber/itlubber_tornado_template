import config
import pandas as pd
from utils.logger import logger

from dbutils.mysql_connect_pool import MysqlConnectPool


conn_pool = MysqlConnectPool(**config.mysql_connect_pool_options)


if __name__ == '__main__':
    sql_query = """
                    select count(1) from third_xinfangjian
                """
    logger.info(conn_pool.get_dict(sql_query))