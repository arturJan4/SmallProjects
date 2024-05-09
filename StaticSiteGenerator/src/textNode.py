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


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextTypes):
    new_nodes = []
    split_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextTypes.TEXT.value:
            # we only split TextNodes of type text
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid Markdown, wrong number of delimiters: {delimiter}")

        for idx, chunk in enumerate(split_text):
            if chunk == "":
                continue

            if idx % 2 == 0:
                # not in delimiter scope
                split_nodes.append(TextNode(chunk, TextTypes.TEXT))
                continue

            split_nodes.append(TextNode(chunk, text_type))

    new_nodes.extend(split_nodes)
    return new_nodes
