import random

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.messenger.components.attachments import TemplateAttachment, VideoAttachment
from apps.messenger.components.buttons import PostbackButton, LoginButton
from apps.messenger.components.elements import ListElement, Element, ReceiptElement, ReceiptAddress, Summary, \
    Adjustment
from apps.messenger.components.messages import Message
from apps.messenger.components.requests import MessageRequest
from apps.messenger.components.templates import ListTemplate, GenericTemplate, ReceiptTemplate
from apps.messenger.components.replies import QuickReplies, TextReply, LocationReply
from apps.messenger.delivery import constants
from apps.messenger.samples.responses import Components


from apps.delivery.models import Promotion, Order, Address, Challenge , Joke ,Pack, Product, ProductUnit, PackDispatch, \
    ProductDispatch


class RepliesMixin(object):

    def __init__(self, event, messenger):
        self.event = event
        self.messenger =  messenger

    def typing(self):
        responses = list()
        responses.append(MessageRequest(self.event.sender, sender_action='mark_seen'))
        responses.append(MessageRequest(self.event.sender, sender_action='typing_on'))
        self.messenger.post_message_queue(responses)
        

    def make_answer(self, sender, answer):
        responses = list()
        responses.append(Components.typing(responses, self.event.sender))
        message = Message(text=answer)
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_start(self):

        self.typing()
        self.machine.set_state(constants.START)
        responses = list()
        message = Message(text="Hola, que tal. ¿Que deseas hacer?")
        responses.append(MessageRequest(self.event.sender, message))

        template = ListTemplate(
            elements=[
                ListElement(
                    title="CHUPA2",
                    image_url=self.get_url("/static/img/game-icon.jpg"),
                    subtitle="Juega con tus amigos cumpliendo divertidos y obvio compartiendo.",
                    buttons=[
                        PostbackButton(
                            title="JUGAR",
                            payload=constants.SHOW_GAME
                        )
                    ],
                ),
                ListElement(
                    title="CHISTES",
                    image_url=self.get_url("/static/img/joke-icon.jpg"),
                    subtitle="Divierte a tus amigos contandoles los mejores chistes.",
                    buttons=[
                        PostbackButton(
                            title="CUENTAME",
                            payload=constants.SHOW_JOKE
                        )
                    ],
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(Components.typing(responses, self.event.sender))
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)

    # def render_start(self):

    #     self.typing()
    #     responses = list()
    #     message = Message(text="Que deseas hacer?")
    #     responses.append(MessageRequest(self.event.sender, message))

    #     template = ListTemplate(
    #         elements=[
    #             ListElement(
    #                 title="NUEVO PEDIDO",
    #                 image_url="https://goo.gl/0XU8MV",
    #                 subtitle="Que siga la Fiesta",
    #                 buttons=[
    #                     PostbackButton(
    #                         title="Nuevo Pedido",
    #                         payload=constants.SHOW_ORDER_MENU
    #                     )
    #                 ],
    #             ),
    #             ListElement(
    #                 title="JUGAR CHUPANJI",
    #                 image_url="https://goo.gl/NtYwm6",
    #                 subtitle="jugar",
    #                 buttons=[
    #                     PostbackButton(
    #                         title="Jugar",
    #                         payload=constants.SHOW_GAME
    #                     )
    #                 ],
    #             ),
    #             ListElement(
    #                 title="VER CHISTES",
    #                 image_url="https://goo.gl/g6r9l5",
    #                 subtitle="Diversion",
    #                 buttons=[
    #                     PostbackButton(
    #                         title="Chistes",
    #                         payload=constants.SHOW_JOKE
    #                     )
    #                 ],
    #             ),
    #             ListElement(
    #                 title="AYUDA",
    #                 image_url="https://goo.gl/1cgPFP",
    #                 subtitle="Necesitas Ayuda?",
    #                 buttons=[
    #                     PostbackButton(
    #                         title="Ayuda",
    #                         payload=constants.SHOW_INFO
    #                     )
    #                 ],
    #             )
    #         ]
    #     )
    #     attachment = TemplateAttachment(template=template)
    #     message = Message(attachment=attachment)
    #     responses.append(Components.typing(responses, self.event.sender))
    #     responses.append(MessageRequest(self.event.sender, message))
    #     self.messenger.post_message_queue(responses)


    def render_info(self):
        self.typing()
        responses = list()
        message = Message(
            text="Hola 👋 😄 con este BOT podras hacer el pedido de bebidas 🍻 y hacer que tu Fiesta 🎉 no se acabe \n"
                 "en el siguiente video te mostramos lo facil que es realizar un pedido 😀"
            )
        responses.append(MessageRequest(self.event.sender, message))

        message = Message(
            attachment=VideoAttachment(
                url="https://www.dropbox.com/s/v5k3jqjpkhccfg7/developer.mp4?dl=1"
            )
        )

        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)
        self.machine.set_state(constants.START)


    def render_login(self):
        template = GenericTemplate(
            elements=[
                Element(
                    title="Iniciar Sesión",
                    subtitle="y Que siga la Fiesta",
                    buttons=[
                        LoginButton(
                            url=self.get_url("/facebook/authorize/%s/" % self.event.sender.id)
                        )
                    ]
                )
            ]
        )

        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        response =  MessageRequest(self.event.sender, message)
        self.messenger.post_message(response)


    def render_logged_in(self):
        responses = list()
        message = Message(text=" Login con Exito 😄")
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_order_menu(self):
        # TODO ESTE ESTADO ATAJO CUANDO ACABE EL DESARROLLO
        # self.machine.set_state(constants.PACK_LIST)
        # self.render_pack_list()
        # return True
        # TODO --------------------------------------------


        self.typing()
        responses = list()
        message = Message(text="Que vas a realizar ?")
        responses.append(MessageRequest(self.event.sender, message))

        template = ListTemplate(
            elements=[
                ListElement(
                    title="HACER NUEVO PEDIDO",
                    image_url="https://goo.gl/sG035S",
                    subtitle="Haz un nuevo pedido",
                    buttons=[
                        PostbackButton(
                            title="PEDIR",
                            payload=constants.SHOW_NEW_ORDER
                        )
                    ],
                ),
                ListElement(
                    title="VER MIS PEDIDOS",
                    image_url="https://goo.gl/sG035S",
                    subtitle="Ve tus pedidos pasados",
                    buttons=[
                        PostbackButton(
                            title="VER PEDIDOS",
                            payload=constants.SHOW_ORDER_LIST
                        )
                    ],
                ),
                ListElement(
                    title="VER PEDIDOS EN CURSO",
                    image_url="https://goo.gl/sG035S",
                    subtitle="Verifica donde esta tu pedido",
                    buttons=[
                        PostbackButton(
                            title="VER PEDIDOS",
                            payload=constants.SHOW_ORDERS_TRACKING
                        )
                    ],
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(Components.typing(responses, self.event.sender))
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_new_order(self):
        self.typing()
        responses = list()
        message = Message(text="Estupendo 😄!!  para continuar necesitamos verificar tu identidad 👤. "
                               "Por favor escribe tu número de celular  📱 para empezar 🏃 🏃 🏃.")

        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)

    def render_order_list(self):
        # TODO CAMBIAR ESTE COMPONENTE POR UNO DE VERDAD
        self.typing()
        responses = list()
        message = Message(text="Lista de Pedidos")
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)

    def render_orders_tracking(self):
        # TODO CAMBIAR ESTE COMPONENTE POR UNO DE VERDAD
        self.typing()
        responses = list()
        message = Message(text="Lista de Ordenes")
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)



    def render_process_code(self):
        self.typing()
        responses = list()
        message = Message(text="Bien 😄, En breve recibiras un código PIN, escríbelo aqui "
                               "para verificar tu número 🏃.")
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_product_menu(self):

        self.typing()
        responses = list()
        message = Message(text="Elige lo que deseas pedir...")
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)

        responses = list()
        template = ListTemplate(
            elements=[
                ListElement(
                    title="UNIDADES",
                    image_url="https://goo.gl/2w8SQV",
                    subtitle="La mejor selección de bebidas",
                    buttons=[
                        PostbackButton(
                            title="VER BEBIDAS",
                            payload=constants.SHOW_UNITS
                        )
                    ],
                ),
                ListElement(
                    title="COMBOS",
                    image_url="https://goo.gl/ZzVa89",
                    subtitle="La mejor combinacion para tu fiesta unida en un pack",
                    buttons=[
                        PostbackButton(
                            title="VER COMBOS",
                            payload=constants.SHOW_PACKS
                        )
                    ],
                )
            ]
        )
        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_search_item(self):
        responses = list()
        elements = []
        message = Message(text="Escribe lo que estas buscando... (Ej. Ron Abuelo)")
        responses.append(MessageRequest(self.event.sender, message))

        packs = Pack.objects.all()

        if packs.count() > 0:
            message = Message(text="Encontramos lo que querias ")
            responses.append(MessageRequest(self.event.sender, message))

            for pack in packs:
                element = Element(
                    title=pack.name,
                    image_url="https://goo.gl/VWsKgb",
                    subtitle=pack.description,
                    buttons=[
                        PostbackButton(
                            title="AGREGAR AL CARRITO",
                            payload="%(trigger)s|%(model)s|%(id)s"%{
                                "trigger": constants.ADD,
                                "model": constants.PACK_MODEL,
                                "id": pack.id
                            }
                        ),
                        PostbackButton(
                            title="CONTINUAR",
                            payload=constants.SHOW_ADDRESS_MENU
                        ),
                    ]
                )
                elements.append(element)
            template = GenericTemplate(
                elements=elements
            )
            attachment = TemplateAttachment(template=template)
            message = Message(attachment=attachment)
            responses.append(Components.typing(responses, self.event.sender))
            responses.append(MessageRequest(self.event.sender, message))
        else:
            self.typing()
            responses = list()
            replies = QuickReplies(
                replies=[
                    TextReply(
                        image_url="https://goo.gl/Rg33Yq",
                        title="MENU INICIO",
                        payload=constants.START,
                    )
                ]
            )
            message = Message(
                text="Ups, 😱 lamentamos decirte que no se encontro el producto",
                quick_replies=replies
            )
            responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_pack_list(self):
        self.typing()
        packs = Pack.objects.all()
        responses = list()
        elements = []

        if packs.count() > 0:
            message = Message(text="Tenemos un stock muy actualizado, aqui te muestro los Packs", )
            responses.append(MessageRequest(self.event.sender, message))

            for pack in packs:
                element = Element(
                    title=pack.name,
                    image_url="https://goo.gl/VWsKgb",
                    subtitle=pack.description,
                    buttons=[
                        PostbackButton(
                            title="AGREGAR AL CARRITO",
                            payload="%(trigger)s|%(model)s|%(id)s"%{
                                "trigger": constants.ADD,
                                "model": constants.PACK_MODEL,
                                "id": pack.id
                            }
                        ),
                        PostbackButton(
                            title="CONTINUAR",
                            payload=constants.SHOW_ADDRESS_MENU
                        ),
                    ]
                )
                elements.append(element)
            template = GenericTemplate(
                elements=elements
            )
            attachment = TemplateAttachment(template=template)
            message = Message(attachment=attachment)
            responses.append(Components.typing(responses, self.event.sender))
            responses.append(MessageRequest(self.event.sender, message))
        else:
            self.typing()
            responses = list()
            replies = QuickReplies(
                replies=[
                    TextReply(
                        image_url="https://goo.gl/Rg33Yq",
                        title="MENU INICIO",
                        payload=constants.START,
                    )
                ]
            )
            message = Message(
                text="Ups, 😱 lamentamos decirte que no hay combos registrados",
                quick_replies=replies
            )
            responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_address_menu(self):
        self.typing()
        responses = list()
        replies = QuickReplies(
            replies=[
                TextReply(
                    image_url="https://goo.gl/uQXzpP",
                    title="VER MIS DIRECCIONES",
                    payload=constants.SHOW_ADDRESS_LIST,
                ),
                LocationReply(),

                TextReply(
                    image_url="https://goo.gl/6t7mb7",
                    title="CANCELAR",
                    payload=constants.START,
                ),
            ]
        )
        message = Message(
            text="¿A donde te enviamos el pedido?",
            quick_replies=replies
        )
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)

    def render_address_list(self):
        self.typing()

        print("\n\n\n\n USUARIO", self.event.user, "\n\n\n\n")
        addresses = Address.objects.filter(user=self.event.user)

        responses = list()
        elements = []

        if addresses.count() > 0:
            message = Message(text="Escoge una alguna de tus direcciones")
            responses.append(MessageRequest(self.event.sender, message))

            for item in addresses:
                element = Element(
                    title=item.alias,
                    item_url=self.get_map_url(item.location),
                    image_url=self.get_map_screen(item.location),
                    subtitle=item.address,
                    buttons=[
                        PostbackButton(
                            title="USAR ESTA DIRECCIÓN",
                            payload="%(trigger)s|%(model)s|%(id)s" % {
                                "trigger": constants.ADDRESS,
                                "model": constants.SHIPPING_ADDRESS_MODEL,
                                "id": item.id
                            }
                        ),
                        PostbackButton(
                            title="CANCELAR",
                            payload=constants.CANCEL
                        ),
                    ]
                )
                elements.append(element)
            template = GenericTemplate(
                elements=elements
            )
            attachment = TemplateAttachment(template=template)
            message = Message(attachment=attachment)
            responses.append(Components.typing(responses, self.event.sender))
            responses.append(MessageRequest(self.event.sender, message))
        else:
            self.typing()
            responses = list()
            replies = QuickReplies(
                replies=[
                    TextReply(
                        image_url="https://goo.gl/Rg33Yq",
                        title="MENU INICIO",
                        payload=constants.START,
                    )
                ]
            )
            message = Message(
                text="Ups, 😱 lamentamos decirte que no tienes direcciones registradas",
                quick_replies=replies
            )
            responses.append(MessageRequest(self.event.sender, message))

        self.messenger.post_message_queue(responses)



    def render_order_detail(self):
        responses = list()

        elements =[]
        summary_price = 0
        shipping_cost = 10
        taxes_cost = 0

        cart = self.session["store"]["cart"]
        user = self.event.user
        order = Order(customer=user)

        if user and user.first_name and user.last_name:
            user_name = "%s %s" % (user.first_name, user.last_name)
        else:
            user_name = "Sin Nombre"


        # Set Address
        street_1, city, state = "", "", ""
        if "shipping_location" in self.session["store"]:
            print("\n\n\n\n ES LOCALIZACION: ", self.session["store"]["shipping_location"], "\n\n\n\n")
            street_1, city, state = "Ubicación proporcionada", "La Paz", "Centro"
            order.location = self.session["store"]["shipping_location"]

        elif "shipping_address" in self.session["store"]:
            print("\n\n\n\n ES DIRECCION: ", self.session["store"]["shipping_address"], "\n\n\n\n")
            item = Address.objects.get(id=int(self.session["store"]["shipping_address"]))
            street_1, city, state = item.address, item.city, item.zone
            order.customer_address = item

        order.save()
        # Set Prices
        for item in cart:
            quantity = int(item["quantity"])

            if item["model"] == constants.PACK_MODEL:
                instance = Pack.objects.get(id=item["pk"])
                for i in range(quantity):
                    dispatch = PackDispatch(order=order, pack=instance)
                    dispatch.save()
            elif item["model"] == constants.PRODUCT_MODEL:
                instance = Product.objects.get(id=item["pk"])
                for i in range(quantity):
                    dispatch = ProductDispatch(order=order, product=instance)
                    dispatch.save()

            price = instance.price
            title = "(%s) %s" % (quantity, instance.comertial_name)
            subtitle = instance.comertial_name
            image = self.get_url(instance.image.url)

            elements.append(
                ReceiptElement(
                    title=title,
                    subtitle=subtitle,
                    quantity=quantity,
                    price=price,
                    currency="BOB",
                    image_url=image
                )
            )
            summary_price += (price * quantity)

        template = ReceiptTemplate(
            recipient_name=user_name,
            order_number=order.code,
            currency="BOB",
            payment_method=order.payment,
            order_url="http://victoraguilar.net",
            timestamp="%s" % int(order.date.timestamp()),
            elements=elements,
            address=ReceiptAddress(
                street_1=street_1,
                street_2="",
                city=city,
                postal_code="000",
                state=state,
                country="BO"
            ),

            summary=Summary(
                subtotal=summary_price,
                shipping_cost=shipping_cost,
                total_tax=taxes_cost,
                total_cost=(summary_price + shipping_cost + taxes_cost),
            ),
            adjustments=[
                # Adjustment(
                #     name="New Customer Discount",
                #     amount=20,
                # ),
                # Adjustment(
                #     name="$10 Off Coupon",
                #     amount=10,
                # )
            ]
        )

        self.store_value("pending_order", order.id)

        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)

        responses.append(MessageRequest(self.event.sender, message))

        self.typing()
        message = Message(
            text="Dale click en CONFIRMAR para terminar el pedido o CANCELAR para volver al inicio",
            quick_replies=QuickReplies(
                replies=[
                    TextReply(
                        title="Confirmar",
                        payload=constants.CONFIRM,
                        image_url='https://goo.gl/hjz4rk'
                    ),
                    TextReply(
                        title="Cancelar",
                        payload=constants.CANCEL,
                        image_url='https://goo.gl/6t7mb7'
                    )
                ]
            )
        )
        responses.append(MessageRequest(self.event.sender, message))

        self.messenger.post_message_queue(responses)


    def render_success_message(self):
        responses = list()
        if "pending_order" in self.session["store"]:
            order_id = int(self.store_value("pending_order"))
            order = Order.objects.get(id=order_id)
            text = "Su pedido ha sido confirmado, el número de pedido es %(code)s, puede hacer el seguimiento desde " \
                   "la siguiente dirección %(url)s, o ingresar a pedidos desde el menú." \
                   "Muchas gracias por confiar en nosotros." % {
                        "code": order.code,
                        "url": self.get_url("/orders/%s" % order.code),
                    }
        else:
            text = "No tiene pedidos pendientes."

        message = Message(
            text=text,
            quick_replies=QuickReplies(
                replies=[
                    TextReply(
                        title="HACER OTRO PEDIDO",
                        payload=constants.ORDER_MENU,
                        image_url='https://goo.gl/bfDj2S'
                    ),
                    TextReply(
                        title="TERMINAR",
                        payload=constants.CANCEL,
                        image_url='https://goo.gl/6t7mb7'
                    )
                ]
            )
        )

        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)

    def render_phrase(self):
        pass

    def render_profile_info(self):
        pass


    def render_game_info(self):
        self.typing()
        responses = list()
        elements = []

        challenges = Challenge.objects.all()

        challenges_added = self.store_value("challenges", list())

        for challenge in challenges:
            challenges_added.append({'id':challenge.id,'active':True})


        if challenges.count() > 0:

            element = Element(
                title="CHUPA2",
                image_url=self.get_url("/static/img/game-logo.jpg"),
                subtitle="Agrega a tus amigos y cumple retos divertidos.",
                buttons=[
                    PostbackButton(
                        title="PARTIDA RAPIDA",
                        payload=constants.QUICKPLAY
                    ),
                    PostbackButton(
                        title="AGREGAR AMIGOS",
                        payload=constants.START_GAME
                    ),
                    PostbackButton(
                        title="VOLVER AL INICIO",
                        payload=constants.START
                    ),
                ]
            )
            elements.append(element)
            template = GenericTemplate(
                elements=elements
            )
            attachment = TemplateAttachment(template=template)
            message = Message(attachment=attachment)
            responses.append(Components.typing(responses, self.event.sender))
            responses.append(MessageRequest(self.event.sender, message))

        else:
            message = Message(text=" =( Aún no hay retos disponibles para juego :'(", )
            responses.append(MessageRequest(self.event.sender, message))
            self.machine.set_state(constants.START)

        self.messenger.post_message_queue(responses)

    def render_show_help_game(self):
        self.typing()
        responses = list()
        message = Message(
            text=" =) Como Jugar ❓ \n"
                 " . \n"
                 " 1⃣ Selecciona COMENZAR \n"
                 " 2⃣ Agregar a tus amigos\n"
                 " 3⃣ Cumple los Retos\n"
                 " QUE SIGA LA FIESTA TE RECOMIENDA \n"
                 " 🍸 Disfruta Responsablemente. \n"
                 " 🔑 Si vas a tomar, pasa las llaves. \n"
                 " 👍 Juego para mayores de Edad\n"
            )
        responses.append(MessageRequest(self.event.sender, message))

        replies = QuickReplies(
            replies=[
                TextReply(
                    image_url="https://goo.gl/Rg33Yq",
                    title="JUGAR",
                    payload=constants.START_GAME
                ),
                TextReply(
                    image_url="https://goo.gl/u4OR8c",
                    title="MENU INICIO",
                    payload=constants.START
                ),

            ]
        )
        message = Message(
            text=" =) ",
            quick_replies=replies
        )
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)


    def render_process_players(self):
        responses = list()
        self.typing()

        if hasattr(self, "player_added"):
            text = "👤 " + (self.player_added).upper() + ", ha sido agregado al 🎲 JUEGO."
        else:
            message = Message(text="Agrega a tus amig@s 👥, escribe su nombre y presiona ▶ enviar o enter.")
            responses.append(MessageRequest(self.event.sender, message))
            text = "Cuando hayas agregado a todos tus amig@s presiona ▶ EMPEZAR RETO"

        replies = QuickReplies(
            replies=[
                TextReply(
                    image_url="https://goo.gl/Rg33Yq",
                    title="EMPEZAR RETO",
                    payload=constants.START_CHALLENGES
                ),
                TextReply(
                    image_url="https://goo.gl/u4OR8c",
                    title="CANCELAR",
                    payload=constants.START
                ),

            ]
        )
        message = Message(
            text=text,
            quick_replies=replies
        )
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)



    def render_challenge(self):
        responses = list()
        elements = []

        players = self.session["store"]["players"]
        challenges = self.session["store"]["challenges"]

        def verify_true(challenges):
            sw = 0
            for challenge in challenges:
                if challenge['active'] == True:
                    return True

        answer_verify_true = verify_true(challenges)

        if answer_verify_true:
            for challenge in challenges:
                if challenge['active'] == True:
                    _select_id = challenge['id']
                    challenge['active'] = False
                    break
                    
        else:
            for challenge in challenges:
                challenge['active'] = True

            for challenge in challenges:
                challenge['active'] == True
                _select_id = challenge['id']
                challenge['active'] = False
                break


        _challenge = Challenge.objects.get(id=_select_id)

        what_players = _challenge.get_who_display()

        select_player = list()

        for player in players:
            select_player.append(player['user'])

        _user = random.choice(select_player)


        def increase_suck(_user, players):
            for player in players:
                if player['user'] == _user:
                    print("JUGADOR TOMA ", player['user'])
                    previous_suck = player['suck']
                    player['suck'] = previous_suck + 1

        def increase_suck_all(players):
            print("TODOS TOMAN")
            for player in players:
                previous_suck = player['suck']
                player['suck'] = previous_suck + 1

        def increase_suck_saved(_user, players):
            for player in players:
                if player['user'] == _user:
                    print("Jugador salvado ", player['user'])
                else:
                    previous_suck = player['suck']
                    player['suck'] = previous_suck + 1


        if what_players == "Una persona":
            text = "Jugador : 👤 " + (_user).upper() + "\n " + _challenge.challenge + "🍺"

        elif what_players == "Todos":
            increase_suck_all(players)
            text = _challenge.challenge
            
        elif what_players == "Jugador toma":
            increase_suck(_user ,players)
            text = "Jugador : 👤 " + (_user).upper() + "\n " + _challenge.challenge + "🍺"

        elif what_players == "Jugador salvado":
            increase_suck_saved(_user, players)
            text = "Jugador : 👤 " + (_user).upper() + "\n " + _challenge.challenge + "🍺"

        else:
            text = _challenge.challenge

        element = Element(
            title=_challenge.get_category_display(),
            image_url=self.get_url(_challenge.image.url),
            subtitle="Cantidad de sorbos: " + _challenge.suck,
            buttons=[
                PostbackButton(
                    title="SIGUIENTE RETO",
                    payload=constants.NEW_CHALLENGE,
                ),
                PostbackButton(
                    title="TERMINAR JUEGO",
                    payload=constants.RANKING_SUCKS,
                ),
            ]
        )
        elements.append(element)
        template = GenericTemplate(
            elements=elements
        )

        self.typing()

        message = Message(text=" 😁 " + _challenge.name.upper())
        responses.append(MessageRequest(self.event.sender, message))

        message = Message(text=text)
        responses.append(MessageRequest(self.event.sender, message))

        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(Components.typing(responses, self.event.sender))
        responses.append(MessageRequest(self.event.sender, message))
    
        self.messenger.post_message_queue(responses)


    def render_challenge_fast(self):
        responses = list()
        elements = []
        
        challenges = self.session["store"]["challenges"]

        def verify_true(challenges):
            for challenge in challenges:
                if challenge['active'] == True:
                    return True

        answer_verify_true = verify_true(challenges)

        if answer_verify_true:
            for challenge in challenges:
                if challenge['active'] == True:
                    _select_id = challenge['id']
                    challenge['active'] = False
                    break
                    
        else:
            for challenge in challenges:
                challenge['active'] = True

            for challenge in challenges:
                challenge['active'] == True
                _select_id = challenge['id']
                challenge['active'] = False
                break

        _challenge = Challenge.objects.get(id=_select_id)


        element = Element(
            title=_challenge.get_category_display(),
            image_url=self.get_url(_challenge.image.url),
            subtitle="Cantidad de sorbos: " + _challenge.suck,
            buttons=[
                PostbackButton(
                    title="SIGUIENTE RETO",
                    payload=constants.NEW_CHALLENGE_FAST,
                ),
                PostbackButton(
                    title="TERMINAR JUEGO",
                    payload=constants.CANCEL_CHALLENGE_FAST,
                ),
            ]
        )
        elements.append(element)
        template = GenericTemplate(
            elements=elements
        )
        self.typing()
        message = Message(text=" 😁 " + _challenge.name.upper())
        responses.append(MessageRequest(self.event.sender, message))

        message = Message(text=_challenge.challenge)
        responses.append(MessageRequest(self.event.sender, message))

        attachment = TemplateAttachment(template=template)
        message = Message(attachment=attachment)
        responses.append(Components.typing(responses, self.event.sender))
        responses.append(MessageRequest(self.event.sender, message))
    
        self.messenger.post_message_queue(responses)


    def render_show_ranking_sucks(self):
        responses = list()
        self.typing()

        message = Message(text="😎 Lista de Jugadores Chupa2")
        responses.append(MessageRequest(self.event.sender, message))

        players_list = self.session["store"]["players"]

        list_players = ""

        for player in players_list:
            list_players = list_players + " 👤 " + str(player['user']) + " Sorbos  " +  (str(player['suck']) + "\n")


        message = Message(text=list_players)
        responses.append(MessageRequest(self.event.sender, message))

        replies = QuickReplies(
            replies=[
                TextReply(
                    image_url="https://goo.gl/Rg33Yq",
                    title="VOLVER A JUGAR",
                    payload=constants.START_CHALLENGES
                ),
                TextReply(
                    image_url="https://goo.gl/u4OR8c",
                    title="MENU INICIO",
                    payload=constants.CANCEL_CHALLENGE
                ),

            ]
        )
        message = Message(
            text="😄 Gracias por jugar Chupa2 🎲",
            quick_replies=replies
        )
        responses.append(MessageRequest(self.event.sender, message))

        self.messenger.post_message_queue(responses)


    def render_joke(self):
        elements = []
        responses = list()

        jokes = Joke.objects.all()

        if jokes.count() > 0:

            _joke = random.choice(jokes)

            _emoticon = ['😜' ,'😝','😂', '😅', '😆', '😁']

            message = Message(text= _joke.name + random.choice(_emoticon))
            responses.append(MessageRequest(self.event.sender, message))

            element = Element(
                title="Ja ja ja ... ",
                image_url="",
                subtitle="",
                buttons=[
                    PostbackButton(
                        title="OTRO CHISTE",
                        payload=constants.NEW_JOKE,
                    ),
                    PostbackButton(
                        title="TERMINAR",
                        payload=constants.START,
                    ),
                ]
            )
            elements.append(element)
            template = GenericTemplate(
                elements=elements
            )

            self.typing()

            message = Message(text=_joke.joke + "😜 😝 😂")
            responses.append(MessageRequest(self.event.sender, message))

            attachment = TemplateAttachment(template=template)
            message = Message(attachment=attachment)
            responses.append(Components.typing(responses, self.event.sender))
            responses.append(MessageRequest(self.event.sender, message))
        else:
            message = Message(text=" =( no hay chistes disponibles", )
            responses.append(MessageRequest(self.event.sender, message))
            self.machine.set_state(constants.START)

        self.messenger.post_message_queue(responses)


    def render_message(self, text):
        self.typing()
        responses = list()
        message = Message(text=text)
        responses.append(MessageRequest(self.event.sender, message))
        self.messenger.post_message_queue(responses)

# ----------------------------------------------------------------------


    def render_category_list(self):
        # responses = list()
        # message = Message(text="Escribe que tipo de bebida")
        # responses.append(Components.typing(responses, self.event.sender))
        # responses.append(MessageRequest(self.event.sender, message))
        pass



