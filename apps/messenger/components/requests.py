import json
import logging
try:
    import coloredlogs
    coloredlogs.install()
except Exception as e:
    pass


class MessageRequest(object):

    NOTIFICATION_TYPE_OPTIONS = (
        'REGULAR', 'SILENT_PUSH', 'NO_PUSH'
    )

    SENDER_ACTIONS = (
        'typing_on', 'typing_off', 'mark_seen'
    )

    def __init__(self, recipient, message=None, sender_action=None, notification_type=None):
        self.recipient = recipient
        self.message = message
        self._notification_type = notification_type
        self._sender_action = sender_action

    @property
    def notification_type(self):
        if self._notification_type:
            if self._notification_type not in self.NOTIFICATION_TYPE_OPTIONS:
                logging.error('ERROR: notification_type valid options: %s' % str(self.NOTIFICATION_TYPE_OPTIONS))
        return self._notification_type

    @property
    def sender_action(self):
        if self._sender_action:
            if self._sender_action not in self.SENDER_ACTIONS:
                logging.error('ERROR: sender_action valid options: %s' % str(self.SENDER_ACTIONS))
        return self._sender_action

    def to_dict(self):
        data = dict()

        data['recipient'] = self.recipient.to_dict()

        if self.message:
            data['message'] = self.message.to_dict()
        elif self.sender_action:
            data['sender_action'] = self.sender_action

        if self.notification_type:
            data['notification_type'] = self.notification_type

        return data

    def serialise(self):
        return json.dumps(self.to_dict())


class SettingsRequest(object):
    setting_type = None

    def to_dict(self):
        data = dict()
        data['setting_type'] = self.setting_type
        return data

    def serialise(self):
        return json.dumps(self.to_dict())


class AccountLinking(SettingsRequest):
    setting_type = "account_linking"

    ACTION_TYPES = ['add', 'remove']

    def __init__(self, account_linking_url=None):
        self.account_linking_url = account_linking_url

    def to_dict(self):
        data = super(AccountLinking, self).to_dict()
        if self.account_linking_url:
            data['account_linking_url'] = self.account_linking_url
        return data


class DomainWhiteListing(SettingsRequest):

    ACTIONS = ["add", "remove"]
    setting_type = "domain_whitelisting"

    def __init__(self, whitelisted_domains=None, domain_action_type="add"):
        if not whitelisted_domains and isinstance(whitelisted_domains, list):
            logging.error('ERROR: whitelisted_domains is required and as list')

        self.whitelisted_domains = whitelisted_domains
        self.domain_action_type = domain_action_type

    def to_dict(self):
        data = super(DomainWhiteListing, self).to_dict()
        if self.whitelisted_domains:
            data['whitelisted_domains'] = self.whitelisted_domains
        data['domain_action_type'] = self.domain_action_type
        return data


class Greeting(SettingsRequest):
    setting_type = "greeting"

    def __init__(self, greeting=None):
        self.greeting = greeting

    def to_dict(self):
        data = dict()
        if self.greeting:
            data['greeting'] = self.greeting
        return data


# TODO Add full support to facebook payments
class Payment(SettingsRequest):
    setting_type = "payment"

    def __init__(self, payment_privacy_url=None):
        self.payment_privacy_url = payment_privacy_url

    def to_dict(self):
        data = dict()
        if self.payment_privacy_url:
            data['payment_privacy_url'] = self.payment_privacy_url
        return data


class CallToActions(SettingsRequest):
    setting_type = "call_to_actions"
    thread_state = None

    def to_dict(self):
        data = super(CallToActions, self).to_dict()
        data['thread_state'] = self.thread_state
        return data


class StartButton(CallToActions):
    thread_state = "new_thread"

    def __init__(self, call_to_actions=None):

        logging.info(call_to_actions)

        if call_to_actions and not isinstance(call_to_actions, list):
            logging.error('ERROR: call_to_actions debe ser una lista de cadenas')
        if call_to_actions and len(call_to_actions) == 1:
            logging.error('ERROR: el numero de call_to_actions debe ser uno')

        self.call_to_actions = call_to_actions

    def to_dict(self):
        data = super(StartButton, self).to_dict()
        data['call_to_actions'] = [
            button.to_dict() for button in self.call_to_actions
        ]
        return data


class MenuItem(object):
    RATIO_COMPACT = "compact"
    RATIO_TALL = "tall"
    RATIO_FULL = "full"
    TYPE_WEB_URL = "web_url"
    TYPE_POSTBACK = "postback"
    WEB_URL = "web_url"

    MENU_TYPES = [TYPE_WEB_URL, TYPE_POSTBACK]
    WEB_RATIOS = [RATIO_COMPACT, RATIO_TALL, RATIO_FULL]

    def __init__(self, type=None, title=None, url=None, payload=None,
                 webview_height_ratio=None, messenger_extensions=False):

        if webview_height_ratio and webview_height_ratio not in self.WEB_RATIOS:
            logging.error('webview_height_ratio invalido valores permitidos {compact, tall, full}')

        if type and type not in self.MENU_TYPES:
            logging.error('type invalido valores permitidos {web_url, postback}')

        if title and not len(title) <= 30:
            logging.error('El limite para title es 30')

        if payload and not len(payload) <= 1000:
            logging.error('El limite para payload es 1000')

        self.type = type
        self.title = title
        self.url = url
        self.payload = payload
        self.webview_height_ratio = webview_height_ratio
        self.messenger_extensions = messenger_extensions

    def to_dict(self):
        data = dict()
        if self.type:
            data["type"] = self.type

        if self.title:
            data["title"] = self.title

        if self.url:
            data["url"] = self.url

        if self.payload:
            data["payload"] = self.payload

        if self.webview_height_ratio:
            data["webview_height_ratio"] = self.webview_height_ratio

        if self.messenger_extensions:
            data["messenger_extensions"] = self.messenger_extensions

        return data


class ContinousMenu(CallToActions):
    thread_state = "existing_thread"

    def __init__(self, call_to_actions=None):
        if call_to_actions:
            if not isinstance(call_to_actions, list):
                logging.error('ERROR: call_to_actions debe ser nua lista de cadenas')
            for item in call_to_actions:
                if not isinstance(item, MenuItem):
                    logging.error('ERROR: los items deben ser de tipo MenuItem')

        self.call_to_actions = call_to_actions

    def to_dict(self):
        data = super(ContinousMenu, self).to_dict()
        if self.call_to_actions:
            data['call_to_actions'] = [
                menu.to_dict() for menu in self.call_to_actions
            ]
        return data




