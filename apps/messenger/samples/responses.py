from django.conf import settings

from apps.messenger.components.attachments import TemplateAttachment, ImageAttachment, VideoAttachment
from apps.messenger.components.buttons import PostbackButton, URLButton
from apps.messenger.components.elements import ListElement, Element
from apps.messenger.components.messages import Message
from apps.messenger.components.replies import QuickReplies, TextReply, LocationReply
from apps.messenger.components.requests import MessageRequest
from apps.messenger.components.templates import ButtonTemplate, ListTemplate, GenericTemplate

from apps.delivery.models import Promotion, Order

import logging

try:
    import coloredlogs

    coloredlogs.install()
except Exception as e:
    pass

DEFAULT_VIDEO = "https://www.dropbox.com/s/v5k3jqjpkhccfg7/developer.mp4?dl=1"
TOKEN_REQUEST = "TOKEN_REQUEST"
HELP_RESOURCES = [
    {
        "name": TOKEN_REQUEST,
        "url": "https://www.dropbox.com/s/v5k3jqjpkhccfg7/developer.mp4?dl=1"
    }
]

if settings.DEBUG:
    SERVER_URL = "https://484db321.ngrok.io"
else:
    SERVER_URL = "https://chuspita.net"

LOGIN_URL = SERVER_URL+ "/messenger/login/"

class HelpMedia(object):
    @staticmethod
    def get(sender, resource):
        if resource in HELP_RESOURCES:
            url = HELP_RESOURCES[resource]["url"]
        else:
            url = DEFAULT_VIDEO

        message = Message(
            attachment=VideoAttachment(
                url=url
            )
        )
        return MessageRequest(sender, message)


class Components(object):

    @staticmethod
    def typing(requests, sender):
        requests.append(MessageRequest(sender, sender_action='mark_seen'))
        requests.append(MessageRequest(sender, sender_action='typing_on'))

    @staticmethod
    def make_answer(sender, answer):
        responses = list()
        responses.append(Components.typing(responses, sender))
        message = Message(text=answer)
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_welcome(sender):
        responses = list()
        responses.append(Components.typing(responses, sender))
        message = Message(text="Bienvenido Terricola")
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_distance(sender):
        responses = list()
        responses.append(Components.typing(responses, sender))
        message = Message(text="Estas a 5km/10min caminando de distancia de la sucursal")
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_start(sender):
        # Mensaje
        responses = list()
        message = Message(text="Ya no mas filas en el banco")
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))

        template = ListTemplate(
            style="compact",
            elements=[
                ListElement(
                    title="GENERAR UN TICKET",
                    image_url="https://s14.postimg.org/u9ohxgqsd/obtener.png",
                    subtitle="Ahorra tiempo con tickets electrónicos",
                    buttons=[
                        PostbackButton(
                            title="OBTENER TICKET",
                            payload="GET_TICKET"
                        )
                    ],
                ),
                ListElement(
                    title="MIS TICKETS",
                    image_url="https://s14.postimg.org/ea5udwuql/mistickets.png",
                    subtitle="Administra los tickets pendientes que tienes",
                    buttons=[
                        PostbackButton(
                            title="VER MIS TICKETS",
                            payload="MY_TICKETS"
                        )
                    ],
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses

# >>>>>>>>>>>>>>>>>>>>>>>>>> START RECHARGE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    @staticmethod
    def make_init(sender):
        responses = list()
        responses.append(Components.typing(responses, sender))
        message = Message(text="Bienvenido Terricola")
        responses.append(MessageRequest(sender, message))
        return responses


    @staticmethod
    def make_number_phones(sender):
        print("pase x aqui")
        telephone_numbers = None
        responses = list()
        elements = []
        if telephone_numbers.count() > 0:
            for telephone_number in telephone_numbers:
                text = TextReply(
                            title=telephone_number.number,
                            payload="VIEW_BRANCHES",
                            image_url='http://www.teslasrl.net/imagenes/trabajos/ENTEL.jpg'
                        )

                elements.append(text)

            numbers = QuickReplies(
                replies=elements
            )

            message = Message(
                text="Estos son tus numeros ... ",
                quick_replies=numbers
            )

            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))
            return responses
        else:
            message = Message(text="No tienes numeros registrados :(")
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))
            return responses


    @staticmethod
    def recharge_amount(sender):
        responses = list()
        replies = QuickReplies(
            replies=[
                    TextReply(
                        title="10",
                        payload="VIEW_BRANCHES",
                    ),
                    TextReply(
                        title="20",
                        payload="VIEW_BRANCHES",
                    ),
                    TextReply(
                        title="30",
                        payload="VIEW_BRANCHES",
                    ),
                    TextReply(
                        title="50",
                        payload="VIEW_BRANCHES",
                    ),
                    TextReply(
                        title="100",
                        payload="VIEW_BRANCHES",
                    )
            ]
        )

        message = Message(
            text="Cuanto Deseas Recargar?",
            quick_replies=replies
        )
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses


    @staticmethod
    def show_cards(sender):
        # Mensaje
        responses = list()
        message = Message(text="Ya no mas filas en el banco")
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))

        template = ListTemplate(
            style="compact",
            elements=[
                ListElement(
                    title="GENERAR UN TICKET",
                    image_url="https://s14.postimg.org/u9ohxgqsd/obtener.png",
                    subtitle="Ahorra tiempo con tickets electrónicos",
                    buttons=[
                        PostbackButton(
                            title="OBTENER TICKET",
                            payload="GET_TICKET"
                        )
                    ],
                ),
                ListElement(
                    title="MIS TICKETS",
                    image_url="https://s14.postimg.org/ea5udwuql/mistickets.png",
                    subtitle="Administra los tickets pendientes que tienes",
                    buttons=[
                        PostbackButton(
                            title="VER MIS TICKETS",
                            payload="MY_TICKETS"
                        )
                    ],
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses



    @staticmethod
    def make_recharge(sender):
        responses = list()
        responses.append(Components.typing(responses, sender))
        template = GenericTemplate(
            elements=[
                Element(
                    title="Se Recargo con exito 50 Bs al 73053045",
                    subtitle="Gracias por usar el servicio",

                    buttons=[
                        URLButton(
                            title="INICIO",
                            url="https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
                        ),
                        URLButton(
                            title="HACER OTRA RECARGA",
                            url="https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
                        )
                    ]
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        component = Message(attachment=attachment)
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, component))
        return responses

    @staticmethod
    def insufficient_balance(sender):
        responses = list()
        responses.append(Components.typing(responses, sender))
        template = GenericTemplate(
            elements=[
                Element(
                    title="Saldo insuficiente para recargar",
                    subtitle="Advertencia",

                    buttons=[
                        URLButton(
                            title="OTRA RECARGA",
                            url="https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
                        ),
                        URLButton(
                            title="CANCELAR",
                            url="https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
                        )
                    ]
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        component = Message(attachment=attachment)
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, component))
        return responses

    # >>>>>>>>>>>>>>>>>>>>>>>>>> END RECHARGE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    @staticmethod
    def make_position_request(sender):
        # Mensaje y Componente
        responses = list()
        replies = QuickReplies(
            replies=[
                LocationReply(),
                TextReply(
                    title="VER CAJEROS",
                    payload="VIEW_BRANCHES",
                )
            ]
        )

        message = Message(
            text="Por favor envianos tu ubicación para determinar que sucursales estan cerca de ti",
            quick_replies=replies
        )
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def get_map_screen(lat, lng):
        return "https://maps.googleapis.com/maps/api/staticmap?zoom=15&size=500x250&markers=color:red%7Clabel:S%7C" + str(
            lat) \
               + "," + str(lng) + "&key=AIzaSyBwHPJ6_aVyk9QNkzMIPRoC22QFnvnHjME"

    @staticmethod
    def get_map_url(lat, lng):
        return "https://maps.google.com/maps?q=" + str(lat) + "," + str(lng)

    @staticmethod
    def get_position(number):
        geo = str(number.position).split(",")
        return geo[0], geo[1]

    @staticmethod
    def make_branches(sender):
        """
        Envia la lista de Suscripciones de un usuario o la peticion para registrar una suscripción
        """
        branches = None
        responses = list()
        elements = []
        if branches.count() > 0:
            # Mensaje
            message = Message(text="Esta es la lista de Sucursales Cerca :)", )
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))

            # Componente
            for branch in branches:
                lat, lng = Components.get_position(branch)
                element = Element(
                    title=branch.name,
                    item_url=Components.get_map_url(lat, lng),
                    image_url=Components.get_map_screen(lat, lng),
                    subtitle=branch.address,
                    buttons=[
                        PostbackButton(
                            title="VER",
                            payload="%(payload)s:%(id)s" % {
                                "payload": "SELECT_BRANCH",
                                "id": branch.id
                            }
                        )
                    ]
                )
                elements.append(element)
            template = GenericTemplate(
                elements=elements
            )

            attachment = TemplateAttachment(template=template)
            component = Message(attachment=attachment)
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, component))

        else:
            message = Message(text="No hay ninguna sucursales registradas :(")
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_atms(sender):
        """
        Envia la lista de Suscripciones de un usuario o la peticion para registrar una suscripción
        """
        branches = None
        responses = list()
        elements = []
        if branches.count() > 0:
            # Mensaje
            message = Message(text="Esta es la lista de Cajeros cerca :)", )
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))

            # Componente
            for branch in branches:
                lat, lng = Components.get_position(branch)
                element = Element(
                    title=branch.name,
                    item_url=Components.get_map_url(lat, lng),
                    image_url=Components.get_map_screen(lat, lng),
                    subtitle=branch.address,
                    buttons=[
                        PostbackButton(
                            title="VER",
                            payload="%(payload)s:%(id)s" % {
                                "payload": "SELECT_BRANCH",
                                "id": branch.id
                            }
                        )
                    ]
                )
                elements.append(element)
            template = GenericTemplate(
                elements=elements
            )

            attachment = TemplateAttachment(template=template)
            component = Message(attachment=attachment)
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, component))

        else:
            message = Message(text="No hay cajeros registrados :(")
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_change(sender):
        responses = list()

        responses.append(Components.typing(responses, sender))
        template = GenericTemplate(
            elements=[
                Element(
                    title="El Dolar Cotiza a 6,929 Bs.",
                    subtitle="1 USD = 6,929 Bs.",
                    default_action=URLButton(
                        url="https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
                    ),
                    buttons=[
                        URLButton(
                            title="VER OTRAS MONEDAS",
                            url="https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
                        )
                    ]
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        component = Message(attachment=attachment)
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, component))
        return responses

    @staticmethod
    def make_schedules(sender):
        # Mensaje
        responses = list()
        message = Message(text="¿Deseas agendar una cita con un asesor?, (y) Estas son las fechas disponibles")
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))

        template = ListTemplate(
            style="compact",
            elements=[
                ListElement(
                    title="21 de Diciembre del 2016",
                    image_url="https://s14.postimg.org/hn996fblp/date.jpg",
                    subtitle="15:00 Hrs",
                    buttons=[
                        PostbackButton(
                            title="AGENDAR",
                            payload="AGENDA_1"
                        )
                    ],
                ),
                ListElement(
                    title="15 de Enero del 2017",
                    image_url="https://s14.postimg.org/hn996fblp/date.jpg",
                    subtitle="19:00 Hrs.",
                    buttons=[
                        PostbackButton(
                            title="AGENDAR",
                            payload="AGENDA_2"
                        )
                    ],
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_ticket(sender, mode=None):
        # Mensaje
        # TODO cambiar las imagenes por tickets generados.
        responses = list()
        message = Message(text="Este es tu ticket, gracias por confiar en Chuspita")
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))

        if mode == "CASH":
            url = "https://s14.postimg.org/j8qdab43h/caja.png"
        elif mode == "PLATFORM":
            url = "https://s14.postimg.org/olf7ofrzx/plataforma.png"
        else:
            url = "https://s14.postimg.org/olf7ofrzx/plataforma.png"

        message = Message(
            attachment=ImageAttachment(
                url=url
            )
        )
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_own_tickets(sender):
        # tickets = Ticket.objects.all()
        tickets = list()
        responses = list()
        elements = []
        if tickets.count() > 0:
            # Mensaje
            message = Message(text="Estos son tus tickets", )
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))

            # Componente
            for ticket in tickets:
                lat, lng = Components.get_position(ticket.branch)
                if ticket.type == "CASH":
                    tty = "CAJA"
                else:
                    tty = "PLATAFORMA"

                element = Element(
                    title="%s: %s" % (tty, ticket.code),
                    subtitle="%s: %s" % (ticket.branch.bank.name, ticket.branch.name),
                    default_action=URLButton(
                        url=Components.get_map_url(lat, lng)
                    ),
                    buttons=[
                        PostbackButton(
                            title="CANCELAR",
                            payload="%(payload)s:%(id)s" % {
                                "payload": "CANCEL_TICKET",
                                "id": ticket.id
                            }
                        ),
                        PostbackButton(
                            title="RENOVAR",
                            payload="%(payload)s:%(id)s" % {
                                "payload": "REGENERATE_TICKET",
                                "id": ticket.id
                            }
                        )
                    ]
                )
                elements.append(element)
            template = GenericTemplate(
                elements=elements
            )

            attachment = TemplateAttachment(template=template)
            component = Message(attachment=attachment)
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, component))

        else:
            message = Message(text="No tienes tickets")
            responses.append(Components.typing(responses, sender))
            responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_cancel_ticket(sender):
        responses = list()
        message = Message(text="Se ha cancelado el ticket que solicitaste :'(", )
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_regenerate_ticket(sender):
        responses = list()
        message = Message(text="Enviame tu ubicación para generar el ticket que mas te convenga ;)")
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))
        return responses

    @staticmethod
    def make_promotions(sender):
        """
        Envia la lista de promociones
        """
        promotions = None
        responses = list()
        elements = []

        # Mensaje
        message = Message(text="Esta es la lista de promociones esta semana :)", )
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, message))

        # Componente
        for promotion in promotions:
            element = Element(
                title=promotion.name,
                item_url=promotion.url,
                image_url=SERVER_URL + promotion.cover.url,
                subtitle=promotion.description,
                buttons=[
                    URLButton(
                        title="VER",
                        url=promotion.url
                    )
                ]
            )
            elements.append(element)
        template = GenericTemplate(
            elements=elements
        )

        attachment = TemplateAttachment(template=template)
        component = Message(attachment=attachment)
        responses.append(Components.typing(responses, sender))
        responses.append(MessageRequest(sender, component))
        return responses
