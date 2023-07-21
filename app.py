# -*- coding: utf8 -*-
import os
import uuid
import logging
from flask import Flask, request
from Enums import *
from Constants import *
from Objects import *
from Services.Messages import process_messages
from datetime import datetime
from Utils import timeit
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                    format=LOG_FORMAT)
log = logging.getLogger()


@app.before_request
def pre_processor():
    g.request_id = str(uuid.uuid4())
    log.addFilter(RequestFilter())
    log.info(request.method + ": " + request.full_path)
    if request.method == HTTPMethods.POST.name:
        log.info(request.json)


@timeit
@app.route("/", methods=[HTTPMethods.GET.name])
def verify():
    print(request.headers)
    if request.args.get(HUB_MODE) == SUBSCRIBE and request.args.get(HUB_CHALLENGE):
        if not request.args.get(HUB_VERIFY_TOKEN) == os.environ[VERIFY_TOKEN]:
            return TOKEN_MISMATCH, HTTPResponseCodes.FORBIDDEN
        return request.args[HUB_CHALLENGE], HTTPResponseCodes.SUCCESS.value
    return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value


@timeit
@app.route("/", methods=["POST"])
def post_messages():
    data = request.json
    log.info(data)

    if "standby" in data["entry"][-1]:
        return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value

    entry = Entry(**data["entry"][-1])
    msg = Messaging(**entry.messaging[-1])
    process_messages(msg)

    return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value


if __name__ == '__main__':
    app.run(debug=True, port=8080)
