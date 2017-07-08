# -*- coding: utf-8 -*-
from . import definitions
from . import base


class Attribute(base.XmlBase):

    def __init__(self, default=definitions.Undefined, required=True):
        base.XmlBase.__init__(
            self, base.StorageType.attribute, default, required)
    __init__.safe_to_replace = True


class StringAttribute(base.StringXmlBase, Attribute):
    pass


class IntegerAttribute(base.IntegerXmlBase, Attribute):
    pass


