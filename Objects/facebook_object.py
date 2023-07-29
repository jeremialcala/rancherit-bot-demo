from .object import Object


# FACEBOOK OBJECTS
class Coordinates(Object):
    def __init__(self, lat, long):
        super().__init__()
        self.lat = lat
        self.long = long


class Payload(Object):
    def __init__(self, url=None, coordinates: Coordinates = None):
        super().__init__()
        self.url = url
        self.coordinates = coordinates


class Attachments(Object):
    def __init__(self, type=None, title=None, url=None, payload=None):
        super().__init__()
        self.title = title
        self.url = url
        self.type = type
        self.payload = payload


class Message(Object):
    def __init__(self, mid=None, seq=None, attachments: list = None, reply_to=None, text=None, is_echo=None,
                 app_id=None, quick_reply=None, sticker_id=None):
        super().__init__()
        self.mid = mid
        self.seq = seq
        self.text = text
        self.attachments = attachments
        self.reply_to = reply_to
        self.is_echo = is_echo
        self.quick_reply = quick_reply
        self.app_id = app_id
        self.sticker_id = sticker_id


class Messaging(Object):
    def __init__(self, sender, recipient, timestamp, message: Message = None, read=None, postback=None,
                 delivery=None):
        super().__init__()
        self.sender = sender
        self.recipient = recipient
        self.timestamp = timestamp
        self.read = read
        self.postback = postback
        self.delivery = delivery
        self.message = message


class Postback(Object):
    def __init__(self, payload, title):
        super().__init__()
        self.payload = payload
        self.title = title


class Entry(Object):
    def __init__(self, id, time, standby: list = None, messaging: list = None):
        super().__init__()
        self.id = id
        self.time = time
        self.standby = standby
        self.messaging = messaging


class Sender(Object):
    def __init__(self, id):
        super().__init__()
        self.id = id


class Element(Object):
    def __init__(self, _id=None, title=None, subtitle=None, buttons: list = None):
        super().__init__()
        self._id = _id
        self.title = title
        self.subtitle = subtitle
        self.buttons = buttons


class Store(Object):
    def __init__(self, _id=None, title=None, image_url=None, subtitle=None, buttons: list = None):
        super().__init__()
        self._id = _id
        self.title = title
        # self.tags = tags
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = buttons

    def get_element(self):
        return json.dumps({"title": self.title, "image_url": self.image_url,
                           "subtitle": self.subtitle, "buttons": self.buttons})


class Product(Object):
    def __init__(self, _id=None, title=None, tags: list = None, store=None, price=None, options: list = None,
                 image_url=None, subtitle=None, buttons: list = None):
        super().__init__()
        self._id = _id
        self.title = title
        self.tags = tags
        self.store = store
        self.price = price
        self.options = options
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = buttons

    def get_element(self):
        return json.dumps({"title": self.title, "image_url": self.image_url,
                           "subtitle": self.subtitle, "buttons": self.buttons})
