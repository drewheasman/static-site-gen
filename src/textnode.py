from enum import Enum


class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type: TextType = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text and
            self.text_type.name == other.text_type.name and
            self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
