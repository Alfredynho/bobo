import logging
import re
try:
    import coloredlogs
    coloredlogs.install()
except Exception as e:
    pass


class Button(object):
    button_type = None
    url = None
    payload = None

    def __init__(self, title=None):
        if title and len(title) > 20:
            logging.error('Button title limit is 20 characters')

        self.title = title

    def to_dict(self):

        data = dict()

        data["type"] = self.button_type
        if self.title:
            data["title"] = self.title

        return data


class URLButton(Button):

    RATIO_COMPACT = "compact"
    RATIO_TALL = "tall"
    RATIO_FULL = "full"
    button_type = 'web_url'
    RATIOS = [RATIO_COMPACT, RATIO_TALL, RATIO_FULL]

    def __init__(self, title=None, url=None, webview_height_ratio="full",
                 messenger_extensions=False, fallback_url=None):

        if not url:
            logging.error('url is required')

        if not(webview_height_ratio in self.RATIOS):
            logging.error('ratio tiene in valor inválido los valores permitidos son: {"compact", "tall", "full"}')

        self.url = url
        self.webview_height_ratio = webview_height_ratio
        self.messenger_extensions = messenger_extensions
        self.fallback_url = fallback_url

        super(URLButton, self).__init__(title=title)

    def to_dict(self):
        data = super(URLButton, self).to_dict()
        if self.webview_height_ratio:
            data["webview_height_ratio"] = self.webview_height_ratio

        data["url"] = self.url
        if self.messenger_extensions:
            data["messenger_extensions"] = self.messenger_extensions

        if self.fallback_url:
            data["fallback_url"] = self.fallback_url
        return data


class PostbackButton(Button):

    button_type = 'postback'

    def __init__(self, title=None, payload=None):
        if not payload:
            logging.error('payload es requerido')
        self.payload = payload
        super(PostbackButton, self).__init__(title=title)

    def to_dict(self):
        data = super(PostbackButton, self).to_dict()
        data["payload"] = self.payload
        return data


class CallButton(PostbackButton):

    button_type = 'phone_number'

    def __init__(self, title=None, payload=None):
        super(CallButton, self).__init__(title=title)
        pattern = re.compile("^\+\d+$")
        if payload and not pattern.match(payload):
            logging.error('payload debe ser un numero de telefono')
            self.payload = payload
        else:
            self.payload = None


class ShareButton(Button):

    button_type = 'element_share'

    def __init__(self):
        super(ShareButton, self).__init__()


class LoginButton(Button):

    button_type = 'account_link'

    def __init__(self, url=None):
        super(LoginButton, self).__init__()
        if not url:
            logging.error('url es requerido')

        self.url = url

    def to_dict(self):
        data = super(LoginButton, self).to_dict()
        if self.url:
            data["url"] = self.url
        return data


class LogoutButton(Button):

    button_type = 'account_unlink'

    def __init__(self):
        super(LogoutButton, self).__init__()
