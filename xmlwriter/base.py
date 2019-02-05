

class Undefined:
    pass


class Base:
    _default = Undefined
    _type = str

    def __init__(self, name=None, default=Undefined):
        self._default = default
        if name:
            self._name = name

