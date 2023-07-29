import logging
from flask import g, has_app_context


class RequestFilter(logging.Filter):
    def filter(self, record):
        if has_app_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = '-'
        return record
    