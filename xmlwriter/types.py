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

