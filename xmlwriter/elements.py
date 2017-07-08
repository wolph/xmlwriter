# -*- coding: utf-8 -*-
from . import definitions
from . import base


class Element(base.XmlBase):

    def __init__(self, default=definitions.Undefined, required=True,
                 tail=True):
        if tail:
            storage_type = base.StorageType.tail
        else:
            storage_type = base.StorageType.head

        base.XmlBase.__init__(self, storage_type, default, required)
    __init__.safe_to_replace = True


class StringElement(base.StringXmlBase, Element):
    pass


class IntegerElement(base.IntegerXmlBase, Element):
    pass


