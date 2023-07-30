import json
from bson import ObjectId
from datetime import datetime
from Constants import TIME_FORMAT


class Object(object):

    def to_json(self):
        for key in self.__dict__.keys():
            if type(self.__dict__[key]) is ObjectId:
                self.__dict__[key] = str(self.__dict__[key])

            if type(self.__dict__[key]) is datetime:
                self.__dict__[key] = self.__dict__[key].strftime(TIME_FORMAT)

        return json.dumps(self.__dict__, sort_keys=False, indent=4, separators=(',', ': '))

    def to_json_obj(self):
        obj = json.loads(self.to_json())
        obj.pop("_id")
        return obj
    