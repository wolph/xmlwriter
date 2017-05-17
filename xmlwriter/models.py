# -*- coding: utf-8 -*-
import collections
import xml.etree.ElementTree as ET

from . import fields


class XmlWriterMeta(type):

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


class XmlWriter(ET.Element, metaclass=XmlWriterMeta):

    def __init__(self, *args, **kwargs):
        for arg, field in zip(args, self._fields):
            assert field not in kwargs, 'Got multiple arguments for %r' % field
            kwargs[field] = arg

        print('args', args)
        print('kwargs', kwargs)
        print('self._fields', self._fields)
        print('self._data', self._data)
        for key, value in kwargs.items():
            self._data[key] = value
            element = ET.SubElement(self, key)
            element.text = str(value)

        ET.Element.__init__(self, self._get_name())

    def _get_name(self):
        return self.__class__.__name__

    def serialize(self):
        return ET.tostring(self, encoding='unicode')

    def __str__(self):
        return self.serialize()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
