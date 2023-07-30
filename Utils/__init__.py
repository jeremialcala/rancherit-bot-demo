import time
import os
import requests
import logging
import json
import pytz
from Enums import HTTPResponseCodes
from functools import wraps
from Constants import *
from Objects.facebook_objects import *
from Objects import Database
from Objects import MemCache
from Objects import User
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, format=LOG_FORMAT)
log = logging.getLogger()


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        log.info(f'Starting {func.__name__}')
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        log.info(f'Function {func.__name__} completed total time:{total_time:.4f} seconds')
        return result

    return timeit_wrapper


@timeit
def get_user_by_id(user_id):
    url = os.environ.get(FB_GRAPH_URL).format(user_id, os.environ[PAGE_ACCESS_TOKEN])
    r = requests.get(url)
    if r.status_code != 200:
        log.error(r.text)
        raise Exception(f"We couldn't get a successful response: '{HTTPResponseCodes(r.status_code).name}'")
    else:
        return r.text


@timeit
def who_send(sender: Sender):
    user = None
    try:
        user = User.get_user_by_id(sender.id)

        if user is None:
            data = json.loads(get_user_by_id(sender.id))
            user = User(**data)
            user.save_user()

    except Exception as e:
        log.error(e.args)
    finally:
        return user


@timeit
def get_concept(text):
    db = Database()
    concepts = []
    try:
        for word in text.split(" "):
            log.info(f"Getting: '{word}' from the dictionary")
            csr = db.get_schema().dictionary.find({"words": str.lower(word)})
            [concepts.append(concept["concept"]) for concept in csr]

    except Exception as e:
        log.error(e.__str__())
    finally:
        db.close_connection()
        return concepts


@timeit
def get_speech(speech_type: str):
    db = Database()
    text = ""
    speech = db.get_schema().speeches.find({"type": speech_type})
    try:
        for elem in speech:
            text = elem["messages"][0]
    except Exception as e:
        log.error(e.__str__())
    finally:
        db.close_connection()
        return text


@timeit
def get_stores(db=Database()):
    elements = []
    csr = db.get_schema().stores.find()

    for elem in csr:
        elem = Store(**elem)
        elements.append(elem.to_json_obj())

    payload = {"template_type": "generic", "elements": elements}
    attachment = {"type": "template", "payload": payload}

    db.close_connection()
    return {"attachment": attachment}


@timeit
def accept_terms_and_cond(sender):
    db = Database()
    mem = MemCache()
    now = datetime.now()
    try:
        user = User(**mem.get_client().get(sender.id))
        if user is not None:
            user["tyc"], user["registerStatus"], user["dateTyC"], user["statusDate"] = True, 1, now, now
        else:
            user = db.get_schema().users.find_one({"id": sender.id})

        db.get_schema().users.update_one({"id": sender.id},
                                         {"$set":
                                              {
                                                  "tyc": user["tyc"],
                                                  "registerStatus": user["registerStatus"],
                                                  "dateTyC": now,
                                                  "statusDate": now
                                              }})
        mem.get_client().set(sender.id, user)

    except Exception as e:
        log.error(e.__str__())
    finally:
        mem.close_connection()
        db.close_connection()
    return

