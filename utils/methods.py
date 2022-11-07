from utils.logger import logger
import time


def timer(func):
    def func_wrapper(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        time_spend = time_end - time_start
        logger.info('function {0}() cost time {1} s'.format(func.__name__, time_spend))
        return result

    return func_wrapper