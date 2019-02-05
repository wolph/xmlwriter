from lxml import etree

from . import base
from . import types


class Element(base.Base):
    _element = None

    def __set__(self, instance, value):
        if self._element is None:
            self._element = etree.SubElement(instance, self._name)

        self._element.text = self._from_type(value)

    def __get__(self, instance, owner):
        return self._to_type(self._element.text)


class IntegerElement(Element, types.IntegerTypeMixin):
    pass


class StringElement(Element, types.StringTypeMixin):
    pass


