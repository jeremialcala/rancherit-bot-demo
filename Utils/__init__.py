import time
import os
import requests
import logging
import json
from functools import wraps
from Constants import *
from Objects.facebook_object import *
from Objects import Database
from Objects import MemCache

logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                    format=LOG_FORMAT)
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
        log.info(r.text)
        return r.text
    else:
        return r.text


@timeit
def who_send(sender: Sender):
    mem = MemCache()
    user = None
    try:
        user = mem.get_client().get(sender.id)
        if user is not None:
            return user

        db = Database()
        user = db.get_schema().users.find_one({"id": sender.id})

        if user is None:
            user = json.loads(get_user_by_id(sender.id))
            user["tyc"] = False
            user["registerStatus"] = 0
            user["operationStatus"] = 0
            db.get_schema().users.insert_one(user)
            mem.get_client().set(sender.id, json.dumps(user))

        db.close_connection()
    except Exception as e:
        log.error(e.__str__())
    finally:
        mem.close_connection()
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
    text = "Hola"
    speech = db.get_schema().speeches.find({"type": speech_type})
    try:
        for elem in speech:
            print(elem["messages"][0])
            text = elem["messages"][0]
    except Exception as e:
        print(e.args)
    finally:
        db.close_connection()
        return text


@timeit
def get_stores(user, db=Database()):
    elements = []
    csr = db.get_schema().stores.find()

    for elem in csr:
        elem = Store(**elem)
        elements.append(elem.to_json_obj())

    payload = {"template_type": "generic", "elements": elements}
    attachment = {"type": "template", "payload": payload}

    db.close_connection()

    return {"attachment": attachment}
    # send_message(user["id"], get_speech("store_list"), event)
    # send_attachment(recipient_id=user["id"], message=response, event=event)
