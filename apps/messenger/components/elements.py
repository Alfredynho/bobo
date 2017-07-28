
from apps.messenger.components.buttons import URLButton


class Element(object):

    def __init__(self, title, item_url=None, image_url=None, subtitle=None, buttons=None, default_action=None):

        self._title = title
        self.item_url = item_url
        self.image_url = image_url
        self._subtitle = subtitle
        self._buttons = buttons
        self.default_action = default_action

    @property
    def title(self):
        if len(self._title) > 45:
            raise ValueError('title no puede tener mas de 45 caracteres')
        return self._title

    @property
    def subtitle(self):
        if self._subtitle:
            if len(self._subtitle) > 80:
                raise ValueError('El Subtitule no puede tener mas de 80 caracteres')
        return self._subtitle

    @property
    def buttons(self):
        return self._buttons

    def to_dict(self):

        data = dict()
        if self.title:
            data["title"] = self.title

        if self.item_url:
            data["item_url"] = self.item_url

        if self.image_url:
            data["image_url"] = self.image_url

        if self.subtitle:
            data["subtitle"] = self.subtitle

        if self.default_action:
            data["default_action"] = self.default_action.to_dict()

        if self.buttons:
            data['buttons'] = [
                button.to_dict() for button in self.buttons
            ]
        return data


class ListElement(Element):

    def __init__(self, title=None, item_url=None, image_url=None, subtitle=None, buttons=None, default_action=None):

        if item_url and default_action:
            raise ValueError('No puedes tener las propiedades item_url y default_action al mismo tiempo')

        if not item_url and default_action and not isinstance(default_action, URLButton):
            raise ValueError('default_action debe ser de tipo URLButton')

        self.default_action = default_action

        super(ListElement, self).__init__(title, item_url, image_url, subtitle, buttons)

    @property
    def buttons(self):
        if len(self._buttons) > 1:
            raise ValueError('El máximo de botones permitido es 1')
        return self._buttons

    def to_dict(self):
        serialised = super(ListElement, self).to_dict()
        if self.default_action and isinstance(self.default_action, URLButton):
            serialised["default_action"] = self.default_action.to_dict()
        return serialised


class ReceiptElement(object):
    def __init__(self, title=None, subtitle=None, quantity=None, price=None, currency=None, image_url=None):
        if not title:
            raise ValueError('title es requerido')
        if not price:
            raise ValueError('price es requerido')
        elif not price > 0:
            raise ValueError('price no puede ser 0 ni negativo')

        self.title = title
        self.subtitle = subtitle
        self.quantity = quantity
        self.price = price
        self.currency = currency
        self.image_url = image_url

    def to_dict(self):
        data = dict()
        data["title"] = self.title
        if self.subtitle:
            data["subtitle"] = self.subtitle
        if self.quantity:
            data["quantity"] = self.quantity
        data["price"] = self.price
        if self.currency:
            data["currency"] = self.currency
        if self.image_url:
            data["image_url"] = self.image_url
        return data


class ReceiptAddress(object):
    def __init__(self, street_1=None, street_2=None, city=None, postal_code=None, state=None, country=None):

        if not street_1:
            raise ValueError('street_1 es requerido')
        if not city:
            raise ValueError('city es requerido')
        if not postal_code:
            raise ValueError('postal_code es requerido')
        if not state:
            raise ValueError('state es requerido')
        if not country:
            raise ValueError('country es requerido')
        self.street_1 = street_1
        self.street_2 = street_2
        self.city = city
        self.postal_code = postal_code
        self.state = state
        self.country = country

    def to_dict(self):
        data = dict()
        data["street_1"] = self.street_1
        if self.street_2:
            data["street_2"] = self.street_2
        data["city"] = self.city
        data["postal_code"] = self.postal_code
        data["state"] = self.state
        data["country"] = self.country
        return data


class Summary(object):
    def __init__(self, subtotal=None, shipping_cost=None, total_tax=None, total_cost=None):

        if not total_cost:
            raise ValueError('total_cost es requerido')

        self.subtotal = subtotal
        self.shipping_cost = shipping_cost
        self.total_tax = total_tax
        self.total_cost = total_cost

    def to_dict(self):
        data = dict()
        if self.subtotal:
            data["subtotal"] = self.subtotal
        if self.shipping_cost:
            data["shipping_cost"] = self.shipping_cost
        if self.total_tax:
            data["total_tax"] = self.total_tax
        data["total_cost"] = self.total_cost

        return data


class Adjustment(object):

    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount

    def to_dict(self):
        data = dict()
        if self.name:
            data["name"] = self.name
        if self.amount:
            data["amount"] = self.amount
        return data



