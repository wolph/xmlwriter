import abc
import inspect
import logging
import collections
from lxml import etree

from . import base
from . import utils


logger = logging.getLogger(__name__)


class ModelMeta(abc.ABCMeta):

    registry = collections.OrderedDict()

    def __prepare__(name, bases):
        return collections.OrderedDict()

    def get_init(fields):
        '''
        Dynamically generate an `__init__` method from a list of fields

        This is a bit of dark magic but still nice if you ask me :)
        '''

        parameters = []
        needs_default = False
        for key, field in fields.items():
            kwargs = dict(name=key)

            # Get the default if available, once we've gotten a single
            # element with a default all the following parameters need defaults
            # or must be keyword only
            if field._default is not base.Undefined:
                needs_default = True
                kwargs['default'] = field._default

            if field._type:
                kwargs['annotation'] = field._type

            if not needs_default or 'default' in kwargs:
                kwargs['kind'] = inspect.Parameter.POSITIONAL_OR_KEYWORD
            else:
                kwargs['kind'] = inspect.Parameter.KEYWORD_ONLY

            parameters.append(inspect.Parameter(**kwargs))

        signature = inspect.Signature(parameters=parameters)

        def __init__(self, *args, **kwargs):
            etree.ElementBase.__init__(self)

            if args or kwargs:
                bound = signature.bind(*args, **kwargs)
                for key, value in bound.arguments.items():
                    field = fields[key]

                    # Handle automatic model to dict conversion
                    if isinstance(value, dict) and issubclass(field, Model):
                        value = field(**value)
                        self.append(value)

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
        fields = collections.OrderedDict()
        for k, v in namespace.items():
            # Skip hidden items
            if k.startswith('_'):
                continue

            if isinstance(v, base.Base):
                fields[k] = v
                if not hasattr(v, '_name'):
                    v._name = k
            elif isinstance(v, ModelMeta):
                fields[utils.camel_to_underscore(k)] = v
                if not hasattr(v, '_name'):
                    v._name = k
            else:
                logger.info('unknown type: %s=%s', k, v)

        init = namespace.get('__init__')
        if init is None:
            namespace['__init__'] = metaclass.get_init(fields)

        cls = abc.ABCMeta.__new__(metaclass, name, bases, namespace)

        full_name = metaclass.get_name(name, namespace)
        if full_name in metaclass.registry:
            raise NameError('Found multiple classes with the name %s' %
                            full_name)
        else:
            metaclass.registry[full_name] = cls

        return cls

    @classmethod
    def __set__(cls, parent, child):
        # If we're adding a child element, append it to the parent
        if isinstance(child, Model) and not child._element:
            parent.append(child)


class Model(base.Base, etree.ElementBase, metaclass=ModelMeta):
    _element = None

    def __set__(self, instance, value):
        print('%s.__set__(%r, %r, %r)' % (
            self.__class__.__name__, self, instance, value))
        if not self._element:
            self._element = etree.SubElement(instance, self._name)

        self._element.text = self._from_type(value)

    def __get__(self, instance, owner):
        print('Model.__get__', self, instance, owner)
        return self._to_type(self._element.text)
