# -*- coding: utf8 -*-
from enum import Enum


class HTTPMethods(Enum):
    GET = 1
    POST = 2
    PUSH = 3
    PUT = 4
    PATCH = 5
    DELETE = 6


class HTTPResponseCodes(Enum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500
    FORBIDDEN = 403
