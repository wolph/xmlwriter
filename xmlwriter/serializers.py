import xml.etree.ElementTree as ET


class Serializer:
    pass


class XmlSerializer(Serializer):

    def serialize(self, element):
        return ET.tostring(element)
