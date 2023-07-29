import time
import os
import requests
import logging
import json
from functools import wraps
from Constants import *
from Objects.facebook_object import *
from Objects import Database

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


def get_user_by_id(user_id):
    url = os.environ.get(FB_GRAPH_URL).format(USER_ID, PAGE_ACCESS_TOKEN)

    r = requests.get(url)
    if r.status_code != 200:
        return r.text
    else:
        return r.text


def who_send(sender: Sender):
    db = Database().get_schema()
    result = db.users.find({"id": sender.id})
    if result.count() == 0:
        user = json.loads(get_user_by_id(sender.id))
        user["tyc"] = False
        user["registerStatus"] = 0
        user["operationStatus"] = 0
        db.users.insert_one(user)
    else:
        return (doc for doc in result)

    return user
