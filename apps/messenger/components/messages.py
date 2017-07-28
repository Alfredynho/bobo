
class Message(object):

    def __init__(self, text=None, attachment=None, quick_replies=None):
        if not text and not attachment and not quick_replies:
            raise ValueError('<Message> text or attachment or quick_replies must be set')

        self.text = text
        self.attachment = attachment
        self.quick_replies = quick_replies

    def to_dict(self):
        data = {}
        if self.text:
            data['text'] = self.text
        if self.attachment:
            data['attachment'] = self.attachment.to_dict()
        if self.quick_replies:
            data['quick_replies'] = self.quick_replies.to_dict()
        return data


class Recipient(object):

    def __init__(self, recipient_id=None, phone_number=None):
        if not recipient_id and not phone_number:
            raise ValueError('<Recipient> id or phone_number must be set')
        self.recipient_id = recipient_id
        self.phone_number = phone_number

    def to_dict(self):
        if self.recipient_id:
            return {'id': self.recipient_id}
        return {'phone_number': self.phone_number}

    @property
    def id(self):
        if self.recipient_id:
            return self.recipient_id
        return self.phone_number

