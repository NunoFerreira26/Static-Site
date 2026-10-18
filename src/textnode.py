from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text #Text content of the node
        self.text_type = text_type #Type of text this node contains (member of TextType)
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return ( #True if all their properties are equal
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url 
        )

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})' 

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "",{"src":text_node.url,"alt":text_node.text})
    else:
        raise Exception("TextType invalid. Please choose one of the following: text, bold, italic, code, link, image")