import re

from apps.messenger.delivery import constants


class ContextMixin(object):

    @property
    def allowed_models(self):
        return [constants.PACK_MODEL, constants.PRODUCT_MODEL]

    def send_queue(self, components):
        for component in components:
            self.messenger.post_message(component)

    def listen_values(self):

        # if self.event.message["text"]:
        #     answer = self.chupa2.get_response(self.event.message["text"])
        #     self.send_queue(RepliesMixin.make_answer(sender, str(answer)))


        if self.state == constants.NEW_ORDER:
            phone = self.event.message["text"]
            is_valid_phone = self.validate_phone(phone)
            if is_valid_phone:
                pin = self.get_pin()
                self.session["store"]["phone"] = phone
                self.session["store"]["pin"] = pin

                print("\n --->>  PIN: ", pin)

            self.valid_phone = is_valid_phone
            self.trigger(constants.SHOW_PROCESS_CODE)

        elif self.state == constants.PROCESS_CODE:
            pin = self.event.message["text"]
            is_valid_pin = self.validate_pin(pin)



            print("\nWRITED PIN : ", pin)

            self.valid_pin = is_valid_pin
            self.trigger(constants.SHOW_PRODUCT_MENU)

        elif self.state == constants.ADDRESS_MENU:
            print("\n")

            if self.event.has_attachments:
                attachments = self.event.attachments
                for attachment in attachments:
                    if attachment["type"] == "location":
                        location = attachment["payload"]["coordinates"]
                        self.store_value("shipping_location", "%s,%s" % (location["lat"], location["long"]))
                        self.trigger(constants.LOCATION)


        elif self.state == constants.PROCESS_PLAYERS:
            player = self.event.message["text"]
            players = self.store_value("players", list())

            def comprueba(_user, players):
                for x in players:
                    if x['user'] == _user.upper():
                        return True

            if comprueba(player,players):
                self.render_message(player + " ya se encuentra registrado prueba con otro nombre 😬")
                self.trigger(constants.ADD_PLAYER)

            else:
                players.append({'user':player.upper(),'suck':0})
                self.player_added = player
                self.trigger(constants.ADD_PLAYER)



    def store_value(self, key=None, value=None):

        if key and key not in self.session["store"]:
            self.session["store"][key] = value
        return self.session["store"][key]



    def get_condition_item(self, collection=None, key_condition=None, value_condition=None, default_item=None):
        for item in collection:
            if item[key_condition] == value_condition:
                return item
        collection.append(default_item)
        return default_item


    def process_payload(self, payload):
        if bool(re.search('[\|]+', payload)):
            vars = payload.split("|")
            payload = vars[0]
            self.save_data(case=vars[1], value=vars[2])
        return payload


    def save_data(self, case=None, value=None):
        print("\n ----> SAVING DATA >>> case: ", case, ", value: ", value)
        if case and value:
            if case == constants.PRODUCT_MODEL or case == constants.PACK_MODEL:
                cart = self.store_value("cart", list())
                promo = self.get_condition_item(
                    collection=cart,
                    key_condition="model",
                    value_condition=case,
                    default_item={
                        "model": case,
                        "pk": value,
                        "quantity": 0
                    }
                )
                promo["quantity"] += 1

            elif case == constants.SHIPPING_ADDRESS_MODEL:
                self.store_value("shipping_address", value)
