
from .object import Object
from bson import ObjectId


class User(Object):
    def __init__(self, first_name, last_name, profile_pic, id, tyc=False, register_status=0, operation_status=0):
        super().__init__()
        self._id = ObjectId()
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic
        self.id = id
        self.tyc = tyc
        self.register_status = register_status
        self.operation_status = operation_status



