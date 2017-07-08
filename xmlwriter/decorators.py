import functools


def XmlRoot(name):
    def xml_root(function):
        function.name = name
        return function

    return xml_root


def XmlType(name):
    def xml_type(function):
        function.name = name
        return function

    return xml_type


def XmlElement(name):
    def xml_element(function):
        function.name = name
        return function

    return xml_element


