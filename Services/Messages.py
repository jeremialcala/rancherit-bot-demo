import logging
import os
import json
import requests
from datetime import datetime
from Constants import *
from Objects import *
from Enums import *
from Utils import timeit
#
params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
headers = {"Content-Type": "application/json"}
logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                    format=LOG_FORMAT)
log = logging.getLogger()


@timeit
def send_message(recipient_id, message_text):
    data = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message_text}})
    print(data)
    requests.post(os.environ["FB_MESSAGES_URL"].format(os.environ["FB_API_VERSION"]),
                  params=params, headers=headers, data=data)


@timeit
def process_messages(msg: Messaging):
    try:
        sender = Sender(**msg.sender)
        message = Message(**msg.message)

        if message.is_echo is not None:
            return HTTPResponseCodes.SUCCESS.value

        send_message(sender.id, message.text)
    except Exception as e:
        log.error(e.__str__())
        return HTTPResponseCodes.SERVER_ERROR.value