# -*- coding: utf-8 -*-
import enum
import itertools
import collections
import xml.etree.ElementTree as ET

from . import definitions

class XmlType(enum.Enum):
    '''The XmlType specifies whether this object should render as attribute,
    before other nodes or after other nodes

    Head/Pre: 
    ```
    <SomeNode>
        <OurElement>our_value</OurElement>
        <ChildNode/>
    </SomeNode>
    ```

    Tail/Post: 
    ```
    <SomeNode>
        <ChildNode/>
        <OurElement>our_value</OurElement>
    </SomeNode>
    ```

    Attribute/Attr: 
    ```
    <SomeNode our_attribute="our_value"/><ChildNode/>
    ```
    '''
    pre = 1
    head = 1
    post = 2
    tail = 2
    attr = 3
    attribute = 3


class XmlBaseMeta(type):

    registry = dict()

    def __prepare__(name, bases):
        return collections.OrderedDict()

    def get_name(name, namespace):
        parts = []
        if namespace.get('__module__'):
            parts.append(namespace.get('__module__'))

        parts.append(name)

        return '.'.join(parts)

    def __new__(metaclass, name, bases, namespace):
        data = namespace.setdefault('_data', {})
        fields = namespace.setdefault('_fields', collections.OrderedDict())
        for k, v in namespace.items():
            if isinstance(v, Field):
                fields[k] = v
                data[k] = v.default

        cls = type.__new__(metaclass, name, bases, namespace)

        full_name = metaclass.get_name(name, namespace)
        if full_name in metaclass.registry:
            raise NameError('Found multiple classes with the name %s' %
                            full_name)
        else:
            metaclass.registry[full_name] = cls

        return cls


class XmlBase(ET.Element):

    def __init__(self, xml_type, default=definitions.Undefined, required=True):
        self.xml_type = xml_type
        self.default = default
        self.required = required

    def __call__(self):
        return self.type(self.get_value())


class StringXmlBase(XmlBase):
    type = str


class IntegerXmlBase(XmlBase):
    type = int
