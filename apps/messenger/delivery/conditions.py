import re

import random

from apps.messenger.delivery import constants
from apps.messenger.models import MessengerSession, MessengerInfo


class ConditionsMixin(object):


    def has_session(self):

        muid = self.event.sender.id
        has_link = MessengerInfo.objects.filter(messenger_id=muid).exists()
        if has_link:
            link = MessengerInfo.objects.get(messenger_id=muid)
            has_session = MessengerSession.objects.filter(info=link, page_id=self.event.recipient.id).exists()
            if has_session:
                return True
        self.trigger(constants.SHOW_LOGIN)
        return False

    def has_valid_phone(self):
        if self.valid_phone:
            return True
        self.render_message("El número que escribiste no es válido, por favor intenta nuevamente."
        "escribe tu número de celular  📱 para empezar 🏃 🏃 🏃.")
        return False

    def has_valid_pin(self):
        if self.valid_pin:
            return True
        self.render_message("El número de PIN es inválido")
        return False

    def has_cart(self):
        if "cart" in self.session["store"]:
            return True
        self.render_message("No tienes nada en el Carrito")
        return False

    def has_players(self):
        if "players" in self.session["store"]:
            return True
        self.render_message(" 😱 Si quieres comenzar el juego debes agregar a tus amig@s")
        self.trigger(constants.PROCESS_PLAYERS)
        return False

    def validate_phone(self, phone):
        pattern = re.compile("^[7|6][0-9]{7}$")
        valid = pattern.match(phone)
        return bool(valid)

    def validate_pin(self, pin):
        saved_pin = str(self.session["store"]["pin"])
        pin = str(pin)

        print("\nSAVED_PIN: ", saved_pin," WRITED_PIN: ", pin)
        print("\nCOPARISON: ", (saved_pin == pin))
        print("\nSTATE: ", self.state)

        return pin == saved_pin


    def get_pin(self, length=5):
        """ Return a numeric PIN with length digits """
        return random.sample(range(10 ** (length - 1), 10 ** length), 1)[0]

    def verify_pin(self, mobile_number, pin):
        """ Verify a PIN is correct """
        if self.session["pin"]:
            return pin == self.session["pin"]
        return False