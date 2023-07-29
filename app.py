# -*- coding: utf8 -*-
import os
import uuid
import logging
from flask import Flask, request, g
from Enums import *
from Constants import *
from Objects.facebook_object import *
from Objects.request_filter import RequestFilter
from Services.Messages import process_messages
from Utils import timeit


app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                    format=LOG_FORMAT)
log = logging.getLogger()


@app.before_request
@timeit
def pre_processor():
    g.request_id = str(uuid.uuid4())
    log.addFilter(RequestFilter())
    log.info(request.method + ": " + request.full_path)


@app.route("/", methods=[HTTPMethods.GET.name])
@timeit
def verify():
    print(request.headers)
    if request.args.get(HUB_MODE) == SUBSCRIBE and request.args.get(HUB_CHALLENGE):
        if not request.args.get(HUB_VERIFY_TOKEN) == os.environ[VERIFY_TOKEN]:
            return TOKEN_MISMATCH, HTTPResponseCodes.FORBIDDEN
        return request.args[HUB_CHALLENGE], HTTPResponseCodes.SUCCESS.value
    return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value


@app.route("/", methods=["POST"])
@timeit
def post_messages():
    data = request.json
    log.info(data)

    if STAND_BY in data["entry"][-1]:
        return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value

    entry = Entry(**data["entry"][-1])
    msg = Messaging(**entry.messaging[-1])
    process_messages(msg)

    return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value


if __name__ == '__main__':
    app.run(debug=True, port=8080)
