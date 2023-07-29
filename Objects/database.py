import pymongo
import os
from .object import Object
from Constants import *


class Database(Object):
    def __init__(self, schema=os.environ.get(SCHEMA)):
        super().__init__()
        self.schema = schema
        self.client = pymongo.MongoClient(os.environ.get(MONGO))
        self.db = self.client[schema]

    def get_schema(self):
        return self.db
