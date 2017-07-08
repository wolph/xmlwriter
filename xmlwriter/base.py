# -*- coding: utf-8 -*-
import abc
import enum
import inspect
import itertools
import collections
import xml.etree.ElementTree as ET

from . import definitions
from . import utils

class StorageType(enum.Enum):
    '''The Type specifies whether this object should render as attribute,
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
    text = 1
    post = 2
    tail = 2
    attr = 3
    attribute = 3


class _XmlBaseBase:
    '''Dummy class so our metaclass can type-check properly'''


class XmlBaseMeta(abc.ABCMeta):

    registry = dict()

    def __prepare__(name, bases):
        return collections.OrderedDict()

    def get_init(fields):
        '''
        Dynamically generate an `__init__` method from a list of fields

        This is a bit of dark magic but still nice if you cask me :)
        '''

        parameters = []
        for key, field in fields.items():
            parameter = inspect.Parameter(
                key,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )

            if field._type:
                parameter = parameter.replace(annotation=field._type)

            if field._default is not definitions.Undefined:
                parameter = parameter.replace(default=field._default)

            parameters.append(parameter)

        signature = inspect.Signature(parameters=parameters)

        def __init__(self, *args, **kwargs):
            if args or kwargs:
                bound = signature.bind(*args, **kwargs)
                for key, value in bound.arguments.items():
                    setattr(self, key, value)

        __init__.__signature__ = signature

        return __init__

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
            if isinstance(v, _XmlBaseBase):
                fields[k] = v
                if not hasattr(v, '_name'):
                    v._name = k
            elif inspect.isclass(v) and issubclass(v, _XmlBaseBase):
                fields[utils.camel_to_underscore(k)] = v
                if not hasattr(v, '_name'):
                    v._name = k
            elif not k.startswith('_'):
                print('unknown type', k, v)

        init = namespace.get('__init__')
        if not init or getattr(init, 'safe_to_replace', False):
            namespace['__init__'] = metaclass.get_init(fields)
            print('new init', name, namespace['__init__'])
        else:
            print('not replacing', name)
        # if getattr(base, '__init__', False) == namespace.get('__init__'):
        #         break
        # print('init', namespace['__init__'])
        # print(namespace)

        cls = abc.ABCMeta.__new__(metaclass, name, bases, namespace)

        full_name = metaclass.get_name(name, namespace)
        if full_name in metaclass.registry:
            raise NameError('Found multiple classes with the name %s' %
                            full_name)
        else:
            metaclass.registry[full_name] = cls

        return cls


class XmlBase(_XmlBaseBase, metaclass=XmlBaseMeta):

    _type = None
    _default = definitions.Undefined


    def __init__(self, storage_type, default=definitions.Undefined, required=True):
        self._storage_type = storage_type
        self._default = default
        self._required = required
        self._data = definitions.Undefined
    # If the __init__ method has `safe_to_replace` enabled it will
    # automatically be overwitten by the metaclass when needed
    __init__.safe_to_replace = True

    def _get_element(self, value):
        element = ET.Element(self._name)
        if self._storage_type is StorageType.text:
            element.text = value
        elif self._storage_type is StorageType.tail:
            element.tail = value

    def iter(self):
        root = ET.Element(self._name)

        for key, value in self._fields.items():
            yield key
            print('%s :: %s' % (key, value))

    # def __call__(self):
    #     return self._type(self.get_value())

    # @abc.abstractmethod
    def _cast(self, value):
        raise NotImplemented


class StringXmlBase(XmlBase):
    _type = str


class IntegerXmlBase(XmlBase):
    _type = int
