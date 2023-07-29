import logging
import os
import json
import requests
from datetime import datetime
from Constants import *
from Objects.facebook_object import *
from Enums import *
from Utils import timeit, who_send, get_concept, get_speech
#
params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
headers = {"Content-Type": "application/json"}
logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                    format=LOG_FORMAT)
log = logging.getLogger()


@timeit
def send_message(recipient_id, message_text):
    data = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message_text}})
    log.info(data)
    requests.post(os.environ[FB_MESSAGES_URL].format(os.environ[FB_API_VERSION]),
                  params=params, headers=headers, data=data)


@timeit
def send_options(recipient_id, options, text):
    data = {"recipient": {"id": recipient_id}, "message": {"text": text, "quick_replies": []}}
    for option in options:
        data["message"]["quick_replies"].append(option)
        log.info(json.dumps(data))

    requests.post(os.environ[FB_MESSAGES_URL].format(os.environ[FB_API_VERSION]),
                  params=params, headers=headers, data=json.dumps(data))


@timeit
def send_attachment(recipient_id, message):
    data = {"recipient": {"id": recipient_id}, "message": message}
    requests.post(os.environ[FB_MESSAGES_URL].format(os.environ[FB_API_VERSION]),
                  params=params, headers=headers, data=json.dumps(data))


@timeit
def send_tyc(sender, user):
    msg_text = get_speech("wellcome").format(user["first_name"])
    send_message(sender.id, msg_text)

    # TODO: Create objects to this elements
    button = {"type": "web_url", "title": "+info", "url": os.environ[TYC_URL]}
    element = {"image_url": os.environ[BOT_IMG],
               "title": os.environ[BOT_NAME],
               "subtitle": "Terms and conditions of service",
               "buttons": [button]}

    payload = {"template_type": "generic", "elements": [element]}
    attachment = {"type": "template", "payload": payload}
    response = {"attachment": attachment}
    send_attachment(recipient_id=sender.id, message=response)

    options = [{"content_type": "text", "title": "Yes!", "payload": "ACCEPT_PAYLOAD"},
               {"content_type": "text", "title": "No", "payload": "REJECT_PAYLOAD"}]
    send_options(sender.id, options, get_speech("tyc_request"))


@timeit
def process_messages(msg: Messaging):
    try:
        sender = Sender(**msg.sender)
        message = Message(**msg.message)

        if message.is_echo is not None:
            return HTTPResponseCodes.SUCCESS.value

        user = who_send(sender)

        if user["tyc"] is False:
            send_tyc(sender, user)
            return

        log.info(message.to_json_obj())

        if message.attachments is None:
            concepts = get_concept(message.text)
            log.info(concepts)
            return

        send_message(sender.id, message.text)

    except Exception as e:
        log.error(e.args)
        return HTTPResponseCodes.SERVER_ERROR.value