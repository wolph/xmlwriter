from . import definitions
from . import base

class Field(base.XmlBaseBase):

    def __init__(self, name=None, default=definitions.Undefined, type=str):
        self._name = name
        self._default = default
        self._type = type

    def _to_type(self, value):
        return self._type(value)

    def _to_string(self, value):
        return str(value)


class Attribute(Field):
    pass
