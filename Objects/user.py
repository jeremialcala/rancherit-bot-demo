from datetime import datetime
from pytz import timezone
from bson import ObjectId
from .database import Database
from .memcache import MemCache
from Constants import TZ_INFO, TIME_FORMAT
import os
import json


class User:
    created_at: datetime
    tyc_accepted_date: datetime

    def __init__(self, first_name, last_name, profile_pic, id, _id=ObjectId(), tyc=False,
                 created_at=datetime.now(timezone(os.environ[TZ_INFO])), register_status=0,
                 operation_status=0, tyc_accepted_date=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic
        self.id = id
        self.tyc = tyc
        self.register_status = register_status
        self.operation_status = operation_status
        self.created_at = created_at
        self.tyc_accepted_date = tyc_accepted_date

    def to_json(self):
        for element in self.__dict__:
            if type(self.__dict__[element]) is ObjectId:
                self.__dict__[element] = str(self.__dict__[element])
            if type(self.__dict__[element]) is datetime:
                self.__dict__[element] = self.__dict__[element].strftime("%Y-%m-%d %H:%M:%S %f")

        return json.dumps(self.__dict__, sort_keys=False, indent=4, separators=(',', ': '))

    def accept_tyc(self):
        if not self.tyc:
            self.tyc = True
            self.register_status = 1
            self.tyc_accepted_date = datetime.now(timezone(os.environ[TZ_INFO]))
            db = Database()
            mem = MemCache()
            db.get_schema().users.update_one({"id": self.id},
                                             {
                                                 "$set": {
                                                     "tyc": self.tyc,
                                                     "register_status": self.register_status,
                                                     "tyc_accepted_date": self.tyc_accepted_date
                                                 }
                                             })
            mem.get_client().set(self.id, self.to_json())
            mem.close_connection()
            db.close_connection()

    @staticmethod
    def get_user_by_id(id):
        mem = MemCache()
        data = mem.get_client().get(id)

        if data is not None:
            mem.close_connection()
            return User(**json.loads(data))

        db = Database()
        data = db.get_schema().users.find_one({"id": id})
        if data is not None:
            user = User(**data)
            mem.get_client().set(id, user.to_json())
            mem.close_connection()
            db.close_connection()
            return user

        return None

    def save_user(self):
        mem = MemCache()
        db = Database()
        try:
            mem.get_client().set(self.id, self.to_json())
            db.get_schema().users.insert_one(self.__dict__)
        except Exception as e:
            raise Exception(e)
        finally:
            mem.close_connection()
            db.close_connection()

