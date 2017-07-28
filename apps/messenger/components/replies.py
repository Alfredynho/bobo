import logging
try:
    import coloredlogs
    coloredlogs.install()
except Exception as e:
    pass


class QuickReplies(object):

    def __init__(self, replies=None):

        if len(replies)>10:
            logging.error("quick_replies debe tener 10 o menos elementos")
        self.replies = replies

    def to_dict(self):
        return [
            reply.to_dict() for reply in self.replies
        ]


class Reply(object):
    content_type = "text"
    title = None
    payload = None
    image_url = None

    def to_dict(self):
        data = dict()
        data["content_type"] = self.content_type
        if self.title:
            data["title"] = self.title
        if self.payload:
            data["payload"] = self.payload
        if self.image_url:
            data["image_url"] = self.image_url
        return data


class TextReply(Reply):
    content_type = "text"

    def __init__(self, title=None, payload=None, image_url=None):
        if not title:
            logging.error("quick_replies es requerido")
        else:
            if len(title) > 20:
                logging.error("title no puede tener mas de 20 caracteres")

        if not payload:
            logging.error("payload es requerido")
        else:
            if len(payload) > 1000:
                logging.error("payload no puede tener mas de 1000 caracteres")

        self.title = title
        self.payload = payload
        self.image_url = image_url


class LocationReply(Reply):
    content_type = "location"
