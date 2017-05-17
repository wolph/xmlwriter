# -*- coding: utf-8 -*-
from . import definitions
from . import base


class Attribute(base.XmlBase):

    def __init__(self, default=definitions.Undefined, required=True):
        base.XmlBase.__init__(self, default, required,
                              xml_type=XmlType.attribute)


class StringAttribute(Attribute):
    type = str


class IntegerAttribute(Attribute):
    type = int

