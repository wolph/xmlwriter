# -*- coding: utf-8 -*-
from . import definitions
from . import base


class Element(base.XmlBase):

    def __init__(self, xml_type, default=definitions.Undefined, required=True):
        base.XmlBase.__init__(self, default, required, xml_type)

    def __call__(self):
        return self.type(self.get_value())
