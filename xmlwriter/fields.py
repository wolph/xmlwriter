# -*- coding: utf-8 -*-
import enum
import itertools
import collections

from . import definitions
from . import base


class Element(base.XmlBase):

    def __init__(self, default=definitions.Undefined, required=True,
                 tail=True):
        if tail:
            xml_type = XmlType.tail
        else:
            xml_type = XmlType.head

        base.XmlBase.__init__(self, default, required, xml_type)


class StringElement(Element):
    type = str


class IntegerElement(Element):
    type = int


