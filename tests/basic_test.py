import abc
import inspect
import collections
from lxml import etree


class Undefined:
    pass


class Base:
    _parent = None
    _default = Undefined
    _type = str

    def __init__(self, name=None, default=Undefined):
        self._default = default
        if name:
            self._name = name


class ModelMeta(abc.ABCMeta):

    registry = collections.OrderedDict()

    def __prepare__(name, bases, **kwargs):
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
            if field._default is not Undefined:
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
                # Bind the arguments so all args and kwargs are named correctly
                bound = signature.bind(*args, **kwargs)

                # Apply defaults in case not all arguments were given
                bound.apply_defaults()

                # Set the values to the objects
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

    def __new__(metaclass, name, bases, namespace, collection=None):
        fields = collections.OrderedDict()
        namespace['_fields'] = fields
        namespace['_collection'] = collection

        for k, v in namespace.items():
            # Skip hidden items
            if k.startswith('_'):
                continue

            if isinstance(v, (Base, ModelMeta)):
                fields[k] = v
                if not hasattr(v, '_name'):
                    v._name = k
            else:
                raise RuntimeError('Unknown type for %s: %r' % (k, v))

        init = namespace.get('__init__')
        if init is None:
            namespace['__init__'] = metaclass.get_init(fields)

        cls = abc.ABCMeta.__new__(metaclass, name, bases, namespace)

        for k, v in namespace.items():
            if isinstance(v, ModelMeta):
                v._parent = cls

        full_name = metaclass.get_name(name, namespace)
        if full_name in metaclass.registry:
            raise NameError('Found multiple classes with the name %s' %
                            full_name)
        else:
            metaclass.registry[full_name] = cls

        return cls


class Model(Base, etree.ElementBase, metaclass=ModelMeta):
    _element = None
    _type = dict

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            value = self._fields[key](**value)

        if isinstance(value, Model):
            self.append(value)

        Base.__setattr__(self, key, value)


class TypeMixin:
    @staticmethod
    def _type(value):
        return value

    def _to_type(self, value):
        return self._type(value)

    def _from_type(self, value):
        return str(value)


class IntegerTypeMixin(TypeMixin):
    _type = int


class StringTypeMixin(TypeMixin):
    _type = str


class Attribute(Base):

    def __set__(self, instance, value):
        # Set the attribute to the element
        instance.attrib[self._name] = string_value = self._from_type(value)

        # Make sure it can be converted back to the native type again
        self._to_type(string_value)

    def __get__(self, instance, owner):
        return self._to_type(instance.attrib[self._name])


class IntegerAttribute(IntegerTypeMixin, Attribute):
    pass


class StringAttribute(StringTypeMixin, Attribute):
    pass


class Element(Base):
    _element = None

    def __set__(self, instance, value):
        if self._element is None:
            self._element = etree.SubElement(instance, self._name)

        self._element.text = self._from_type(value)

    def __get__(self, instance, owner):
        return self._to_type(self._element.text)


class IntegerElement(IntegerTypeMixin, Element):
    pass


class StringElement(StringTypeMixin, Element):
    pass


class Inline(Base):
    _parent = None
    _tail = None

    def __set__(self, instance, value):
        if not self._parent:
            # Finding the parent of an inline element is a bit tricky, we need
            # to use the tail of the previous element if there is one or the
            # text of the parent element otherwise.
            previous = None
            for k, v in instance._fields.items():
                if v is self:
                    break
                previous = v

            if previous:
                self._tail = True
                self._parent = previous._element
            else:
                self._tail = False
                self._parent = instance

        if self._tail:
            self._parent.tail = self._from_type(value)
        else:
            self._parent.text = self._from_type(value)


class IntegerInline(IntegerTypeMixin, Inline):
    pass


class StringInline(StringTypeMixin, Inline):
    pass


class Employee(Model, collection='employees'):

    pk = IntegerElement()
    first_name = StringElement(default='')
    last_name = StringElement(default='')
    salary = IntegerAttribute()

    class company(Model):
        name = StringElement()

    class address(Model):
        street = StringElement()
        number = IntegerElement()


def test_employee():
    employee = Employee(
        123,
        first_name='Guido',
        last_name='van Rossum',
        salary=1000000,
        address=dict(
            street='Python street',
            number=789,
        ),
        company=Employee.company(
            name='whatever',
        ),
    )

    print('pk: %d' % employee.pk)
    print('first_name: %s' % employee.first_name)
    print('last_name: %s' % employee.last_name)
    print('company name: %s' % employee.company.name)
    print('employee', employee)
    print()

    print(etree.tostring(employee, pretty_print=True).decode('utf-8'))

    employee.salary = 123
    employee.first_name = 'Spam'
    employee.last_name = 'Eggs'
    print(etree.tostring(employee, pretty_print=True).decode('utf-8'))


if __name__ == '__main__':
    test_employee()
