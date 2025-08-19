from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(None, text_node.text)
        return node
    if text_node.text_type == TextType.BOLD:
        node = LeafNode('b', text_node.text)
        return node
    if text_node.text_type == TextType.ITALIC:
        node = LeafNode('i', text_node.text)
        return node
    if text_node.text_type == TextType.CODE:
        node = LeafNode('code', text_node.text)
        return node
    if text_node.text_type == TextType.LINK:
        node = LeafNode('a', text_node.text, {"href": text_node.url})
        return node
    if text_node.text_type == TextType.IMAGE:
        node = LeafNode('img', '', {"src": text_node.url, "alt": text_node.text})
        return node
    raise ValueError(f"invalid text type: {text_node.text_type}")