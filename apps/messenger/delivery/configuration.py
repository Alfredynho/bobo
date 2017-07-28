from datetime import datetime, timedelta
from django.utils.timezone import utc

from apps.messenger.components.attachments import TemplateAttachment, FileAttachment, VideoAttachment, \
    ImageAttachment, AudioAttachment
from apps.messenger.components.buttons import URLButton, PostbackButton, CallButton, ShareButton, \
    LoginButton, LogoutButton
from apps.messenger.components.elements import Element, ListElement, ReceiptElement, ReceiptAddress, Summary, \
    Adjustment
from apps.messenger.components.messages import Message
from apps.messenger.components.requests import AccountLinking, DomainWhiteListing, StartButton, Greeting, \
    ContinousMenu, MenuItem, MessageRequest
from apps.messenger.components.replies import QuickReplies, TextReply, LocationReply
from apps.messenger.components.templates import ButtonTemplate, GenericTemplate, ListTemplate, \
    ReceiptTemplate

from apps.messenger.delivery import constants


def set_continuos_menu():
    return ContinousMenu(
        call_to_actions=[
            MenuItem(
                type=MenuItem.TYPE_POSTBACK,
                title="MI CUENTA",
                payload=contants.MY_ACCOUNT
            ),

            MenuItem(
                type=MenuItem.TYPE_POSTBACK,
                title="MIS PEDIDOS",
                payload=contants.MY_ORDER
            ),
            MenuItem(
                type=MenuItem.TYPE_POSTBACK,
                title="AYUDA",
                payload=contants.HELP
            )
        ]
    )
