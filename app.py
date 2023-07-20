# -*- coding: utf8 -*-
import os
import uuid
import logging
from flask import Flask, request
from Enums import *
from Constants import *
from Objects import *

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


@app.route("/", methods=[HTTPMethods.GET.name])
def verify():
    if request.args.get(HUB_MODE) == SUBSCRIBE and request.args.get(HUB_CHALLENGE):
        if not request.args.get(HUB_VERIFY_TOKEN) == os.environ[VERIFY_TOKEN]:
            return TOKEN_MISMATCH, HTTPResponseCodes.FORBIDDEN
        return request.args[HUB_CHALLENGE], HTTPResponseCodes.SUCCESS.value
    return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value


@app.route("/", methods=["POST"])
def post_messages():
    log.info(request)
    return HTTPResponseCodes.SUCCESS.name, HTTPResponseCodes.SUCCESS.value


if __name__ == '__main__':
    app.run(debug=True, port=8080)
