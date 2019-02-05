from . import base
from . import types


class Attribute(base.Base):

    def __set__(self, instance, value):
        instance.attrib[self._name] = self._from_type(value)

    def __get__(self, instance, owner):
        return instance.attrib[self._name]


class IntegerAttribute(Attribute, types.IntegerTypeMixin):
    pass


class StringAttribute(Attribute, types.StringTypeMixin):
    pass



