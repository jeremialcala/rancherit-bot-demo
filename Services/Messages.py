import os
import json
import requests
from datetime import datetime
from Constants import *
from Objects import *
from Enums import *

#
params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
headers = {"Content-Type": "application/json"}


def send_message(recipient_id, message_text):
    data = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message_text}})
    print(data)
    requests.post(os.environ["FB_MESSAGES_URL"].format(os.environ["FB_API_VERSION"]),
                  params=params, headers=headers, data=data)


def process_messages(msg: Messaging):
    sender = Sender(**msg.sender)

    if msg.message.is_echo is not None:
        return HTTPResponseCodes.SUCCESS.value

    send_message(sender.id, msg.message.text)
