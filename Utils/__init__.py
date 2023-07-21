import time
from functools import wraps
from Constants import *
import logging


logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                    format=LOG_FORMAT)
log = logging.getLogger()


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        log.info(f'Function {func.__name__} completed total time:{total_time:.4f} seconds')
        return result
    return timeit_wrapper

