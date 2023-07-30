from datetime import datetime
from Utils import get_time_zone


class User:
    def __init__(self, first_name, last_name, profile_pic, id, tyc=False, register_status=0, operation_status=0):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic
        self.id = id
        self.tyc = tyc
        self.register_status = register_status
        self.operation_status = operation_status
        self.created_at = datetime.now().strftime(get_time_zone())



