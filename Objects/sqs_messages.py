from .object import Object
from bson import ObjectId


# TODO: create a timestamp for each message this have to be done in a 'MessageSystemAttribute'

'''
    {
        id:ObjectId(),
        MessageBody: <prompt>,
        MessageAttributes:{
            Sender:{
                "StringValue":<FB_ID>,
                "DataType": "String"
            }
        }
    }
    '''


class SQSMessage(Object):
    Id: ObjectId
    MessageBody: str  # this is the prompt
    MessageAttributes: dict  # this manage special attributes, like fb_id

    def __init__(self, message_prompt=None, message_attributes=None):
        self.Id = ObjectId()
        self.MessageBody = message_prompt
        self.MessageAttributes = message_attributes
