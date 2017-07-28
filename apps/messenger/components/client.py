import requests
from apps.messenger.components.requests import MessageRequest, SettingsRequest
from apps.messenger.components.messages import Message


class MessengerException(Exception):
    pass


class MessengerError(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(**kwargs)

    def raise_exception(self):
        raise MessengerException(
            getattr(self, 'error_data', self.message)
        )


class MessengerClient(object):

    GRAPH_API_URL = 'https://graph.facebook.com/v2.8/me'

    def __init__(self, access_token):
        self.access_token = access_token

        self.message_url = "%(base_url)s/messages?access_token=%(page_token)s" % {
            "base_url": self.GRAPH_API_URL,
            "page_token": self.access_token
        }

        self.settings_url = "%(base_url)s/thread_settings?access_token=%(page_token)s" % {
            "base_url": self.GRAPH_API_URL,
            "page_token": self.access_token
        }

    def start(self, recipient):
        self.post_message(MessageRequest(recipient, sender_action='mark_seen'))
        self.post_message(MessageRequest(recipient, sender_action='typing_on'))

    def send(self, request):

        response = None
        if type(request) is list:
            for message in request:
                response = requests.post(
                    url=self.message_url,
                    headers={"Content-Type": "application/json"},
                    data=message.serialise()
                )
                self.print_response(response)
        else:
            response = requests.post(
                url=self.message_url,
                headers={"Content-Type": "application/json"},
                data=request.serialise()
            )
        self.print_response(response)



    def set(self, config):
        if issubclass(config, SettingsRequest):
            response = requests.post(
                url=self.settings_url,
                headers={"Content-Type": "application/json"},
                data=config.serialise()
            )
            self.print_response(response)
        else:
            print("\n Invalid Settings!!")


    def unset(self, settings=None):
        if settings:
            self.post(self.settings_url, settings)
            response = requests.delete(
                self.settings_url, headers={"Content-Type": "application/json"},
                data=settings.serialise()
            )
            self.print_response(response)
        else:
            print("\n Invalid Settings!!")


    def print_response(self, response):
        if response and response.status_code != 200:
            print("\n", response.json()['error'], "\n")
        else:
            print("\n", response.json(), "\n")

    def post(self, url=None, body=None):
        if not url:
            url = self.message_url
        response = requests.post(
            url, headers={"Content-Type": "application/json"},
            data=body.serialise()
        )

        if response.status_code != 200:
            print("\n\n\n\n", response.json()['error'], "\n\n\n\n")
        else:
            return response.json()

    def post_message(self, message=None):
        if message:
            self.post(self.message_url, message)

    def post_message_queue(self, messages):
        for message in messages:
            if message:
                self.post_message(message)

    def post_text(self, sender, text=None):
        if text and sender:
            message = Message(text=text)
            request = MessageRequest(sender, message)
            self.post(self.message_url, request)

    def post_settings(self, settings=None):
        if settings:
            self.post(self.settings_url, settings)

    def get_psid(self, alt):

        params = {
            "access_token": self.access_token,
            "fields": "recipient",
            "account_linking_token": alt
        }

        response = requests.get(self.GRAPH_API_URL, params=params)

        if response.status_code != 200:
            print("\n\n\n\n RESPONSE", response.json(), "\n\n\n\n")

        response = response.json()
        return response["id"], response["recipient"]

    def get_user(self, sender_id):
        response = requests.get('https://graph.facebook.com/v2.6/' + sender_id ,
                    params = {'access_token': self.access_token } )  

        return response.json()


    def subscribe_app(self):
        """
        Subscribe an app to get updates for a page.
        """
        response = requests.post(
            '%s/subscribed_apps' % self.GRAPH_API_URL,
            params={
                'access_token': self.access_token
            }
        )
        return response.status_code == 200

