from apps.messenger.components.elements import ReceiptAddress, Summary, ReceiptElement, Adjustment


class GenericTemplate(object):

    template_type = 'generic'

    def __init__(self, elements=None):
        if not isinstance(elements, list):
            raise ValueError(
                'elements debería ser una lista de Element'
            )
        self._elements = elements

    @property
    def elements(self):
        if len(self._elements) > 12:
            raise ValueError('Muchos elementos en la plantilla')
        return self._elements

    def to_dict(self):
        return {
            'template_type': self.template_type,
            'elements': [
                element.to_dict() for element in self.elements
            ]
        }


class ButtonTemplate(object):

    template_type = 'button'

    def __init__(self, text, buttons):
        self.text = text

        if not isinstance(buttons, list):
            raise ValueError(
                'buttons deberia ser una lista de Button'
            )
        self.buttons = buttons

    def to_dict(self):
        return {
            'template_type': self.template_type,
            'text': self.text,
            'buttons': [
                button.to_dict() for button in self.buttons
            ]
        }


class ListTemplate(object):

    TEMPLATE_STYLES = ["compact", "large"]

    template_type = 'list'

    def __init__(self, style='compact', elements=None, buttons=None):
        if not isinstance(elements, list):
            raise ValueError(
                'Los elementos deberian venir en un array'
            )
        self._elements = elements
        self._buttons = buttons
        self.top_element_style = style

    @property
    def elements(self):
        if len(self._elements) > 10:
            raise ValueError('Hay muchos elementos en la plantilla')
        return self._elements

    @property
    def buttons(self):
        if self._buttons and len(self._buttons) > 1:
            raise ValueError('El máximo de botones permitidos es 1')
        return self._buttons

    def to_dict(self):
        data = dict()
        data["template_type"] = self.template_type
        data["top_element_style"] = self.top_element_style
        if self.buttons:
            data['buttons'] = [
               button.to_dict() for button in self.buttons
            ]

        data['elements'] = [
            element.to_dict() for element in self.elements
        ]
        return data




class ReceiptTemplate(object):

    template_type = "receipt"

    def __init__(self, recipient_name=None, order_number=None, currency="BOB",
                 payment_method=None, order_url=None, timestamp=None, elements=None,
                 address=None, summary=None, adjustments=None):
        if not recipient_name:
            raise ValueError('recipient_name es requerido')

        if not order_number:
            raise ValueError('order_number es requerido')

        if not payment_method:
            raise ValueError('payment_method es requerido')

        if not elements and len(elements) > 0:
            raise ValueError('El recibo debe tener al menos un elemento')
        else:
            for element in elements:
                if not isinstance(element, ReceiptElement):
                    raise ValueError('los elementos deben ser de tipo ReceiptElement')

        if not summary:
            raise ValueError('summary es requerido')
        elif not isinstance(summary, Summary):
            raise ValueError('summary debe ser de tipo Summary')

        if address and not isinstance(address, ReceiptAddress):
            raise ValueError('address debe ser de tipo Address')

        if adjustments:
            for adjustment in adjustments:
                if not isinstance(adjustment, Adjustment):
                    raise ValueError('los adjustments deben ser de tipo Adjustment')

        self.recipient_name = recipient_name
        self.order_number = order_number
        self.currency = currency
        self.payment_method = payment_method
        self.order_url = order_url
        self.timestamp = timestamp
        self.elements = elements
        self.address = address
        self.summary = summary
        self.adjustments = adjustments

    def to_dict(self):

        data = dict()
        data['template_type'] = self.template_type
        data['recipient_name'] = self.recipient_name
        data['order_number'] = self.order_number
        data['currency'] = self.currency
        data['payment_method'] = self.payment_method
        if self.timestamp:
            data['timestamp'] = self.timestamp
        if self.order_url:
            data['order_url'] = self.order_url
        data['elements'] = [
            element.to_dict() for element in self.elements
        ]
        if self.address:
            data['address'] = self.address.to_dict()
        data['summary'] = self.summary.to_dict()
        data['adjustments'] = [
            adjustment.to_dict() for adjustment in self.adjustments
        ]
        return data
