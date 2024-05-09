from enum import StrEnum
from typing import Any

from src.HTMLNode import LeafNode


class TextTypes(StrEnum):
    TEXT = ("text",)
    BOLD = ("bold",)
    ITALIC = ("italic",)
    CODE = ("code",)
    LINK = ("link",)
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: Any) -> bool:
        if self.text != value.text:
            return False
        if self.text_type != value.text_type:
            return False
        if self.url != value.url:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: "TextNode"):
    if text_node.text_type == TextTypes.TEXT.value:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextTypes.BOLD.value:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextTypes.ITALIC.value:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextTypes.CODE.value:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextTypes.LINK.value:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextTypes.IMAGE.value:
        return LeafNode(
            tag="img",
            value="",
            props={"src": text_node.url, "alt": text_node.text},
        )
    raise ValueError(f"Text type ({text_node.text_type}) not recognized")
