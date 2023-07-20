import os
import json
import requests
from datetime import datetime
from Constants import *

#
params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
headers = {"Content-Type": "application/json"}


def send_message(recipient_id, message_text):
    data = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message_text}})
    print(data)
    requests.post(os.environ["FB_MESSAGES_URL"].format(os.environ["FB_API_VERSION"]),
                  params=params, headers=headers, data=data)
