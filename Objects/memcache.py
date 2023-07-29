from pymemcache import Client
from os import environ
from Constants import *


class MemCache:
    def __init__(self):
        self.client = Client(environ[MEMCACHE_HOST], environ[MEMCACHE_PORT])

    def get_client(self):
        return self.client

    def close_connection(self):
        self.client.close()
    