from datetime import datetime
from pytz import timezone
from bson import ObjectId
from .database import Database
from Constants import TZ_INFO, TIME_FORMAT
import os
import json


class User:
    created_at: datetime
    tyc_accepted_date: datetime

    def __init__(self, first_name, last_name, profile_pic, id, _id=ObjectId(), tyc=False, register_status=0, operation_status=0,
                 created_at=datetime.now(timezone(os.environ[TZ_INFO])), tyc_accepted_date=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic
        self.id = id
        self.tyc = tyc
        self.register_status = register_status
        self.operation_status = operation_status
        self.created_at = created_at if type(created_at) is datetime else datetime.strptime(created_at,
                                                                                            os.environ[TIME_FORMAT])
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
            db.get_schema().users.update_one({"id": self.id},
                                             {
                                                 "$set": {
                                                     "tyc": self.tyc,
                                                     "register_status": self.register_status,
                                                     "tyc_accepted_date": self.tyc_accepted_date
                                                 }
                                             })
