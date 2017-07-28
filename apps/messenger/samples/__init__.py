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


def get_message(sender):
    message = Message(text='Hola ............')
    return MessageRequest(sender, message)


def get_button_template(sender):

    template = ButtonTemplate(
        text='Que quieres hacer?',
        buttons=[
            URLButton(
                title='Show website',
                url='https://oepbolivia.xyz/'
            ),
            PostbackButton(
                title='Start chatting',
                payload='USER_DEFINED_PAYLOAD'
            )
        ]
    )
    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def get_generic_template(sender):
    template = GenericTemplate(
        elements=[
            Element(
                title="Welcome to Peter\'s Hats",
                item_url="https://oepbolivia.xyz/",
                image_url="https://upload.wikimedia.org/wikipedia/en/5/5e/Avatar(Neytiri).jpg",
                subtitle="Weve got the right hat for everyone.",
                buttons=[
                    URLButton(
                        url="https://oepbolivia.xyz/",
                        title="View Website"
                    ),
                    PostbackButton(
                        title="Start Chatting",
                        payload="PAYLOAD"
                    )
                ]
            ),
            Element(
                title="HOLA MUNDO",
                item_url="https://oepbolivia.xyz/",
                image_url="https://goo.gl/wODF4W",
                subtitle="Weve got the right hat for everyone.",
                buttons=[
                    URLButton(
                        url="https://oepbolivia.xyz/",
                        title="View Website"
                    ),
                ]
            ),
            Element(
                title="TERCERA PARTE",
                item_url="https://oepbolivia.xyz/",
                image_url="https://goo.gl/wODF4W",
                subtitle="Weve got the right hat for everyone.",
            )

        ]
    )

    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def get_list_template(sender):
    template = ListTemplate(
        style="large",
        elements=[
            ListElement(
                title="Classic T-Shirt Collection",
                image_url="https://goo.gl/tqQNHV",
                subtitle="See all our colors",
                default_action=URLButton(
                    url="https://peterssendreceiveapp.ngrok.io/shop_collection",
                    webview_height_ratio=URLButton.RATIO_TALL,
                ),
                buttons=[
                    URLButton(
                        title="View",
                        url="https://peterssendreceiveapp.ngrok.io/collection",
                        webview_height_ratio=URLButton.RATIO_TALL
                    )
                ],
            ),
            ListElement(
                title="Classic T-Shirt Collection",
                image_url="https://goo.gl/JYkzoW",
                subtitle="100% Cotton, 200% Comfortable",
                default_action=URLButton(
                    url="https://peterssendreceiveapp.ngrok.io/view?item=100",
                    webview_height_ratio=URLButton.RATIO_TALL
                ),
                buttons=[
                    URLButton(
                        title="Shop Now",
                        url="https://peterssendreceiveapp.ngrok.io/shop?item=100",
                        webview_height_ratio=URLButton.RATIO_TALL
                    )
                ],
            ),
            ListElement(
                title="Classic Blue T-Shirt",
                image_url="https://goo.gl/tqQNHV",
                subtitle="100% Cotton, 200% Comfortable",
                default_action=URLButton(
                    url="https://peterssendreceiveapp.ngrok.io/view?item=101",
                    webview_height_ratio=URLButton.RATIO_TALL
                ),
                buttons=[
                    URLButton(
                        title="Shop Now",
                        url="https://peterssendreceiveapp.ngrok.io/collection",
                        webview_height_ratio=URLButton.RATIO_TALL
                    )
                ],
            ),
            ListElement(
                title="Classic Black T-Shirt",
                image_url="https://goo.gl/W2J5rE",
                subtitle="See all our colors",
                default_action=URLButton(
                    url="https://peterssendreceiveapp.ngrok.io/view?item=102",
                    webview_height_ratio=URLButton.RATIO_TALL
                ),
                buttons=[
                    URLButton(
                        title="Shop Now",
                        url="https://peterssendreceiveapp.ngrok.io/collection",
                        webview_height_ratio=URLButton.RATIO_TALL
                    )
                ],
            ),
        ],
        buttons=[
            PostbackButton(
                title="Ver mas",
                payload="UNDEFINED_PAYLOAD"
            )
        ]
    )
    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def get_receipt_template(sender):

    template = ReceiptTemplate(
        recipient_name="Stephane Crozatier",
        order_number="12345678902",
        currency="USD",
        payment_method="Visa 2345",
        order_url="http://petersapparel.parseapp.com/order?order_id=123456",
        timestamp="1428444852",
        elements=[
            ReceiptElement(
                title="Classic White T-Shirt",
                subtitle="100% Soft and Luxurious Cotton",
                quantity=2,
                price=50,
                currency="USD",
                image_url="http://petersapparel.parseapp.com/img/whiteshirt.png"
            ),
            ReceiptElement(
                title="Classic Gray T-Shirt",
                subtitle="100% Soft and Luxurious Cotton",
                quantity=1,
                price=25,
                currency="USD",
                image_url="http://petersapparel.parseapp.com/img/grayshirt.png"
            )
        ],
        address=ReceiptAddress(
            street_1="1 Hacker Way",
            street_2="",
            city="Menlo Park",
            postal_code="94025",
            state="CA",
            country="US",
        ),
        summary=Summary(
            subtotal=75.00,
            shipping_cost=4.95,
            total_tax=6.19,
            total_cost=56.14,
        ),
        adjustments=[
            Adjustment(
                name="New Customer Discount",
                amount=20,
            ),
            Adjustment(
                name="$10 Off Coupon",
                amount=10,
            )
        ]
    )
    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def set_account_linking():
    request = AccountLinking(
        account_linking_url="https://oepbolivia.xyz/oauth?response_type=code&client_id=1234567890&scope=basic"
    )
    print("A", request.serialise())
    return request


def set_domain_whitelisting():

    request = DomainWhiteListing(
        whitelisted_domains=["https://oepbolivia.xyz"],
        domain_action_type=DomainWhiteListing.ADD
    )
    print("DOMAIN LISTING====>>>>>", request.serialise())
    return request


def get_start_button():
    return StartButton(
        call_to_actions=[
            PostbackButton(
                title="EMPEZAR",
                payload="EMPEZANDO"
            )
        ]
    )


def set_start_greeting():
    return Greeting(
        greeting="Un mensaje introductorio"
    )


def set_continuos_menu():
    return ContinousMenu(
        call_to_actions=[
            MenuItem(
                type=MenuItem.TYPE_POSTBACK,
                title="MI CUENTA",
                payload="PAYLOAD_FOR_HELP"
            ),
            MenuItem(
                type=MenuItem.TYPE_POSTBACK,
                title="NUMEROS",
                payload="PAYLOAD_FOR_START_ORDER"
            ),
            MenuItem(
                type=MenuItem.TYPE_WEB_URL,
                title="TARJETAS",
                url="https://oepbolivia.xyz/checkout",
                webview_height_ratio=MenuItem.RATIO_FULL,
                messenger_extensions=True
            ),
            MenuItem(
                type=MenuItem.TYPE_WEB_URL,
                title="AYUDA",
                url="https://oepbolivia.xyz"
            )
        ]
    )


def get_call_button(sender):
    template = ButtonTemplate(
        text="Necesitas llamar al representante?",
        buttons=[
            CallButton(
                title="Llamar al representante",
                payload="+591 73053045"
            )
        ]
    )

    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def get_share_button(sender):
    template = GenericTemplate(
        elements=[
            Element(
                title="Asi deben saber los humanos",
                subtitle="Mientras tanto en otro universo",
                image_url="https://goo.gl/Lg2CHu",
                buttons=[
                    ShareButton()
                ]
            )
        ]
    )

    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def get_login_button(sender):
    template = GenericTemplate(
        elements=[
            Element(
                title="Iniciar Sesión en Chuspita",
                image_url="https://goo.gl/Lg2CHu",
                buttons=[
                    LoginButton(
                        url="https://oepbolivia.xya/login"
                    )
                ]
            )
        ]
    )

    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def get_logout_button(sender):
    template = GenericTemplate(
        elements=[
            Element(
                title="Cerrar Sesión",
                image_url="https://goo.gl/Lg2CHu",
                buttons=[
                    LogoutButton()
                ]
            )
        ]
    )

    attachment = TemplateAttachment(template=template)
    message = Message(attachment=attachment)
    return MessageRequest(sender, message)


def get_quick_text_replies(sender):
    replies = QuickReplies(
        replies=[
            TextReply(
                title="ROJO",
                payload="ROJO_PAYLOAD",
                image_url="https://goo.gl/Ce04uG"
            ),
            TextReply(
                title="VERDE",
                payload="VERDE_PAYLOAD",
                image_url="https://goo.gl/QCmVib"
            )
        ]
    )

    message = Message(
        text="Escoge un color",
        quick_replies=replies
    )
    return MessageRequest(sender, message)


def get_quick_location_reply(sender):

    replies = QuickReplies(
        replies=[
            LocationReply()
        ]
    )
    message = Message(
        text="Envianos tu ubicacion, muajajajaja",
        quick_replies=replies
    )
    return MessageRequest(sender, message)


def get_file(sender):

    message = Message(
        attachment=FileAttachment(
            url="https://yoparticipo.oep.org.bo/files/procesos-electorales/referendo-autonomico-2016/reglamentos/reglamento-referendo.pdf"
        )
    )
    return MessageRequest(sender, message)


def get_video(sender):
    message = Message(
        attachment=VideoAttachment(
            url="https://www.dropbox.com/s/v5k3jqjpkhccfg7/developer.mp4?dl=1"
        )
    )
    return MessageRequest(sender, message)


def get_audio(sender):
    message = Message(
        attachment=AudioAttachment(
            url="https://www.dropbox.com/s/ymoqe9bzgvdx8d9/developer.mp3?dl=1"
        )
    )
    return MessageRequest(sender, message)


def get_image(sender):
    message = Message(
        attachment=ImageAttachment(
            url="https://yoparticipo.oep.org.bo/img/logo.png"
        )
    )
    # http: // giphy.com / embed / l0HlO4vdchLBZNxYc
    return MessageRequest(sender, message)


