import os
import sys
import math
import pymysql


sys.path.append(os.path.dirname(__file__))


# --------------- tornado配置 --------------- #
max_workers = 4
port = 8084
settings = dict(
                    static_path=os.path.join(os.path.dirname(__file__), "static"),
                    debug=True,
                    autoreload=True
                )


# --------------- 数据库连接池配置 --------------- #
mysql_connect_pool_options = dict(
                                    creator=pymysql,
                                    host="localhost",
                                    database="test",
                                    user="root",
                                    password="123456",
                                    port=3306,
                                    maxconnections=math.floor(math.sqrt(max_workers)),
                                    mincached=1,
                                    maxcached=0,
                                    maxshared=0,
                                    blocking=True,
                                    maxusage=None,
                                    setsession=[],
                                    ping=1,
                                    charset='utf8'
                                )


# --------------- 日志配置 --------------- #
log_file = os.path.join(os.path.dirname(__file__), "logs/info.log")
log_format = "[ %(levelname)s ][ %(asctime)s ][ %(filename)s:%(funcName)s:%(lineno)d ] [ %(message)s ]"
log_date_format = '%Y-%m-%d %H:%M:%S'
log_level = "debug"


# --------------- celery配置 --------------- #
class celery_config:
    BROKER_URL = "amqp://itlubber:123456@localhost:8085/wuyi"
    CELERY_RESULT_BACKEND = "amqp://itlubber:123456@localhost:8085/wuyi"
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 5
    CELERY_MAX_CACHED_RESULTS = 5000
    CELERYD_MAX_TASKS_PER_CHILD = 200
    CELERY_DISABLE_RATE_LIMITS = True
    CELERYD_LOG_FORMAT = log_format
    CELERYD_HIJACK_ROOT_LOGGER = False
