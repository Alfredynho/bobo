#
# from apps.messenger.components.requests import MessageRequest
# from apps.messenger.components.attachments import TemplateAttachment, ImageAttachment, VideoAttachment
# from apps.messenger.components.buttons import PostbackButton, URLButton, LoginButton, LogoutButton
# from apps.messenger.components.elements import ListElement, Element, ReceiptElement
# from apps.messenger.components.messages import Message
# from apps.messenger.components.replies import QuickReplies, TextReply, LocationReply
# from apps.messenger.components.templates import ButtonTemplate, ListTemplate, GenericTemplate
# from apps.messenger.delivery import contants
# from apps.users.models import User
#
# from time import gmtime, strftime, localtime
# from django.utils.translation import ugettext_lazy as _
# from datetime import datetime,date
#
# from django.urls import reverse_lazy
# from django.core.urlresolvers import reverse
#
# from django.urls import reverse
# from django.http import HttpResponseRedirect
#
# import math
# from math import log10
#
# import logging
# try:
#     import coloredlogs
#     coloredlogs.install()
# except Exception as e:
#     pass
#
# DEFAULT_VIDEO = "https://www.dropbox.com/s/v5k3jqjpkhccfg7/developer.mp4?dl=1"
# TOKEN_REQUEST = "TOKEN_REQUEST"
# HELP_RESOURCES = [
#     {
#         "name": TOKEN_REQUEST,
#         "url": "https://www.dropbox.com/s/v5k3jqjpkhccfg7/developer.mp4?dl=1"
#     }
# ]
#
# SERVER_URL = "https://fc5fb959.ngrok.io"
#
# class HelpMedia(object):
#
#     @staticmethod
#     def get(sender, resource):
#         if resource in HELP_RESOURCES:
#             url = HELP_RESOURCES[resource]["url"]
#         else:
#             url = DEFAULT_VIDEO
#
#         message = Message(
#             attachment=VideoAttachment(
#                 url=url
#             )
#         )
#         return MessageRequest(sender, message)
#
# class Components(object):
#
#     @staticmethod
#     def typing(requests, sender):
#         requests.append(MessageRequest(sender, sender_action='mark_seen'))
#         requests.append(MessageRequest(sender, sender_action='typing_on'))
#
#     @staticmethod
#     def my_profile(sender, user_session):
#         responses = list()
#
#         if User.objects.filter(username = user_session).exists():
#             # numbers = Phone.objects.filter(owner=user_session)
#             # cards = Card.objects.filter(owner=user_session)
#             responses.append(Components.typing(responses, sender))
#             message = Message(
#                 text="{} el resumen de tu cuenta, tienes {} numeros registrados y {} tarjetas registradas ".format(str(user_session).upper(), numbers.count(), cards.count()),
#                             )
#             responses.append(MessageRequest(sender, message))
#             responses.append(Components.typing(responses, sender))
#             template = GenericTemplate(
#                 elements=[
#                     Element(
#                         title="Hola {}".format(user_session),
#                         subtitle="¿Que deseas hacer?",
#                         buttons=[
#                             URLButton(
#                                 title="VER NUMEROS",
#                                 url="https://www.djangoproject.com/"
#                             ),
#                             URLButton(
#                                 title="VER TARJETAS",
#                                 url="https://www.djangoproject.com/"
#                             ),
#                             PostbackButton(
#                                 title="CERRAR SESION",
#                                 payload=contants.SIGN_OFF,
#                             )
#                         ]
#                     )
#                 ]
#             )
#             attachment = TemplateAttachment(template=template)
#             component = Message(attachment=attachment)
#             responses.append(MessageRequest(sender, component))
#             return responses
#
#
#     @staticmethod
#     def make_welcome(sender):
#         responses = list()
#
#         replies = QuickReplies(
#             replies=[
#                 TextReply(
#                     title="MI CUENTA",
#                     payload=contants.MY_ACCOUNT,
#                 ),
#                 TextReply(
#                     title="RECARGAR",
#                     payload=contants.RECHARGE,
#                 )
#             ]
#         )
#
#         message = Message(
#             text="¿Que deseas hacer?",
#             quick_replies=replies
#         )
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#         return responses
#
#
#     @staticmethod
#     def make_help(sender):
#         responses = list()
#
#         responses.append(Components.typing(responses, sender))
#         message = Message(
#             text="Usuario necesitas ayuda?",
#                         )
#         responses.append(MessageRequest(sender, message))
#         responses.append(Components.typing(responses, sender))
#         template = GenericTemplate(
#             elements=[
#                 Element(
#                     title="Si tienes alguna duda",
#                     subtitle="Puedes ver estos videos y seguir los pasos",
#                     buttons=[
#                         URLButton(
#                             title="COMO AÑADIR PRODUCTO",
#                             url="https://www.djangoproject.com/"
#                         ),
#                         URLButton(
#                             title="COMO HACER PEDIDO",
#                             url="https://www.djangoproject.com/"
#                         ),
#                         URLButton(
#                             title="COMO INICIAR SESION",
#                             url="https://www.djangoproject.com/"
#                         ),
#
#                     ]
#                 )
#             ]
#         )
#         attachment = TemplateAttachment(template=template)
#         component = Message(attachment=attachment)
#         responses.append(MessageRequest(sender, component))
#         return responses
#
#
#     @staticmethod
#     def make_start(sender):
#         responses = list()
#         message = Message(text="Que vas a pedir?")
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#
#         template = ListTemplate(
#             style="compact",
#             elements=[
#                 ListElement(
#                     title="BEBIDAS",
#                     image_url="https://s14.postimg.org/u9ohxgqsd/obtener.png",
#                     subtitle="La mejor selección de bebidas",
#                     buttons=[
#                         PostbackButton(
#                             title="VER BEBIDAS",
#                             payload="postbacks.GET_TICKET"
#                         )
#                     ],
#                 ),
#                 ListElement(
#                     title="TARJETAS",
#                     image_url="https://s14.postimg.org/ea5udwuql/mistickets.png",
#                     subtitle="Podras anadir tarjetas de ENTEL, VIVA, TIGO",
#                     buttons=[
#                         PostbackButton(
#                             title="VER TARJETAS",
#                             payload="postbacks.MY_TICKETS"
#                         )
#                     ],
#                 ),
#                 ListElement(
#                     title="RESACA",
#                     image_url="https://s14.postimg.org/ea5udwuql/mistickets.png",
#                     subtitle="Tienes resaca, tanquilo nosotros podemos ayudarte",
#                     buttons=[
#                         PostbackButton(
#                             title="VER EL SALVAVIDAS",
#                             payload="postbacks.MY_TICKETS"
#                         )
#                     ],
#                 )
#             ]
#         )
#         attachment = TemplateAttachment(template=template)
#         message = Message(attachment=attachment)
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#         return responses
#
#
#     @staticmethod
#     def make_drinks(sender):
#         responses = list()
#         message = Message(text="Puedes elegir nuestras Bebidas y nuestros packs")
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#
#         template = ListTemplate(
#             style="compact",
#             elements=[
#                 ListElement(
#                     title="BEBIDAS POR UNIDAD",
#                     image_url="https://s14.postimg.org/u9ohxgqsd/obtener.png",
#                     subtitle="La mejor selección de bebidas",
#                     buttons=[
#                         PostbackButton(
#                             title="VER BEBIDAS",
#                             payload=triggers.PICK_UNITS
#                         )
#                     ],
#                 ),
#                 ListElement(
#                     title="CATALOGO DE PACKS",
#                     image_url="https://s14.postimg.org/ea5udwuql/mistickets.png",
#                     subtitle="La mejor combinacion para tu fiesta unida en un pack",
#                     buttons=[
#                         PostbackButton(
#                             title="VER PACKS",
#                             payload="postbacks.MY_TICKETS"
#                         )
#                     ],
#                 )
#             ]
#         )
#         attachment = TemplateAttachment(template=template)
#         message = Message(attachment=attachment)
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#         return responses
#
#     @staticmethod
#     def make_branches(sender):
#         responses = list()
#         elements = []
#         if 1 > 0:
#             # Mensaje
#             message = Message(text="En que sucursal quieres sacar un ticket?", )
#             responses.append(Components.typing(responses, sender))
#             responses.append(MessageRequest(sender, message))
#
#             element = Element(
#                 title="dasda",
#                 item_url="https://www.djangoproject.com/",
#                 image_url="http://bebidasycocteles.com/uploads/tia-maria.jpg",
#                 subtitle="mensajesss",
#                 buttons=[
#                     PostbackButton(
#                         title="AÑADIR",
#                         payload="dasdas"
#                     )
#                 ]
#             )
#             elements.append(element)
#             template = GenericTemplate(
#                 elements=elements
#             )
#
#             attachment = TemplateAttachment(template=template)
#             component = Message(attachment=attachment)
#             responses.append(Components.typing(responses, sender))
#             responses.append(MessageRequest(sender, component))
#
#         else:
#             message = Message(text="No hay ninguna sucursal registrada")
#             responses.append(Components.typing(responses, sender))
#             responses.append(MessageRequest(sender, message))
#         return responses
#
#
#     @staticmethod
#     def make_detail(sender):
#         responses = list()
#         replies = QuickReplies(
#             replies=[
#                 TextReply(
#                     title="COMPRAR",
#                     payload="postbacks.VIEW_BRANCHES",
#                 ),
#                 TextReply(
#                     title="AGREGAR MAS",
#                     payload="postbacks.VIEW_BRANCHES",
#                 )
#             ]
#         )
#
#         message = Message(
#             text="Tienes 1 pack carnavelero, 1 singani casa real",
#             quick_replies=replies
#         )
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#         return responses
#
#     @staticmethod
#     def make_order(sender):
#         responses = list()
#         elements = []
#         if 1 > 0:
#             # Mensaje
#             message = Message(text="Detalle",)
#             responses.append(Components.typing(responses, sender))
#             responses.append(MessageRequest(sender, message))
#
#             template = ReceiptElement(
#                 elements=[
#                     Element(
#                         title="Classic White T-Shirt",
#                         subtitle="100% Soft and Luxurious Cotton",
#                         quantity=2,
#                         price=50,
#                         currency="BOB",
#                         image_url="http://petersapparel.parseapp.com/img/whiteshirt.png",
#                     )
#                 ]
#             )
#             elements.append(element)
#             template = ReceiptElement(
#                 elements=elements
#             )
#
#             attachment = TemplateAttachment(template=template)
#             component = Message(attachment=attachment)
#             responses.append(Components.typing(responses, sender))
#             responses.append(MessageRequest(sender, component))
#
#         else:
#             message = Message(text="No hay ninguna sucursal registrada")
#             responses.append(Components.typing(responses, sender))
#             responses.append(MessageRequest(sender, message))
#         return responses
#
#
#
#     @staticmethod
#     def make_location(sender):
#         responses = list()
#         replies = QuickReplies(
#             replies=[
#                 LocationReply(
#
#                 )
#             ]
#         )
#
#         message = Message(
#             text="Envianos tu ubicacion",
#             quick_replies=replies
#         )
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#         return responses
#
#
#     @staticmethod
#     def make_finalize(sender):
#         responses = list()
#         message = Message(
#             text="{user} Ya te enviamos tu pedido, ahora QUE SIGA LA FIESTA !!! ",
#         )
#         responses.append(Components.typing(responses, sender))
#         responses.append(MessageRequest(sender, message))
#         return responses

from django.dispatch import receiver
from datetime import datetime
import time
import json
#
# from apps.messenger.constants import StateManager
# from apps.messenger.delivery.menu import set_continuos_menu
# from apps.messenger.delivery.responses import Components
# from apps.messenger import constants
# from apps.messenger.models import MessengerSession, MessengerInfo
#
# from apps.users.models import User
#
# import datetime
#
# from django.utils.translation import ugettext_lazy as _
#
#
# def next_step(event=None, messenger=None, state=None):
#
#     print("\n\n\n Trace: ", state["trace"] ,"\n Payload:", event.payload ,"\n Store:", state["store"],"\n User:", event.user, "\n\n\n")
#
#     messenger.post_message_queue(Components.make_welcome(event.sender))
#     # messenger.post_message_queue(Components.make_help(event.sender))
#     # messenger.post_message_queue(Components.make_start(event.sender))
#     # messenger.post_message_queue(Components.make_drinks(event.sender))
#     # messenger.post_message_queue(Components.make_branches(event.sender))
#     # messenger.post_message_queue(Components.make_location(event.sender))
#     # messenger.post_message_queue(Components.make_finalize(event.sender))
#     # Set Menu
#     messenger.post_settings(set_continuos_menu())
#
#
#
#
# def process_response(sender, **kwargs):
#     message = kwargs["message"]
#     messenger = kwargs["messenger"]
#     messenger.post_message(message)
