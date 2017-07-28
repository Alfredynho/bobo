
from datetime import datetime

from apps.messenger.components.messages import Recipient
from apps.messenger.models import MessengerInfo ,MessengerSession


class WebhookMessaging(object):

    def __init__(self, sender, recipient, timestamp=None, **kwargs):
        self.sender = Recipient(recipient_id=sender['id'])
        self.recipient = Recipient(recipient_id=recipient['id'])
        if timestamp is not None:
            self.timestamp = datetime.utcfromtimestamp(timestamp / 1000)

        for key, value in kwargs.items():
            self.__dict__['_%s' % key] = value

    @property
    def is_message(self):

        return hasattr(self, '_message') and \
               "quick_reply" not in self.__dict__["_message"]

    @property
    def is_delivery(self):
        return hasattr(self, '_delivery')

    @property
    def is_postback(self):
        return hasattr(self, '_postback')

    @property
    def is_read(self):
        return hasattr(self, '_read')

    @property
    def is_authentication(self):
        return hasattr(self, '_optin')

    @property
    def is_referral(self):
        return hasattr(self, '_referral')

    @property
    def is_checkout_update(self):
        return hasattr(self, '_checkout_update')

    @property
    def is_account_linking(self):
        return hasattr(self, '_account_linking')

    @property
    def is_quick_reply(self):

        if hasattr(self, '_message'):
            return "quick_reply" in self.__dict__["_message"]
        return False

    @property
    def payload(self):
        if self.is_postback:
            return self.postback["payload"]
        elif self.is_quick_reply:
            if "payload" in self.quick_reply:
                return self.quick_reply["payload"]
        return None

    @property
    def message(self):
        if self.is_message:
            return self.__dict__["_message"]
        return None

    @property
    def postback(self):
        if self.is_postback:
            return self.__dict__["_postback"]
        return None

    @property
    def quick_reply(self):
        if self.is_quick_reply:
            return self.__dict__["_message"]["quick_reply"]
        return None

    @property
    def account_linking(self):
        if self.is_account_linking:
            return self.__dict__["_account_linking"]
        return None

    @property
    def has_link(self):
        has_linking = MessengerInfo.objects.filter(
            messenger_id=self.sender.id).exists()
        return has_linking

    @property
    def has_attachments(self):
        if self.is_message:
            if "attachments" in self.__dict__["_message"]:
                return True
        return False

    @property
    def attachments(self):
        if self.has_attachments:
            return self.__dict__["_message"]["attachments"]
        return None

    @property
    def user_info(self):
        if self.has_link:
            link = MessengerInfo.objects.get(
                messenger_id=self.sender.id)
            return link
        return None

    @property
    def has_session(self):
        muid = self.sender.id
        has_link = MessengerInfo.objects.filter(messenger_id=muid).exists()
        if has_link:
            link = MessengerInfo.objects.get(messenger_id=muid)
            has_session = MessengerSession.objects.filter(info=link, page_id=self.recipient.id).exists()
            if has_session:
                return True
        return False

    @property
    def user(self):
        if self.has_session:
            info = MessengerInfo.objects.get(messenger_id=self.sender.id)
            return info.user
        else:
            return None

    @property
    def data(self):
        return self.__dict__

        
class WebhookEntry(object):

    def __init__(self, id, time, messaging):
        self.id = id
        self.time = datetime.utcfromtimestamp(time / 1000)
        self.messaging = [
            WebhookMessaging(**each)
            for each in messaging
        ]


class Webhook(object):

    def __init__(self, payload):
        self.payload = payload

    @property
    def entries(self):
        return [
            WebhookEntry(**entry)
            for entry in self.payload['entry']
        ]
