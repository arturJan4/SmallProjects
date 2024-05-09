from enum import StrEnum
from typing import Any

from src.HTMLNode import LeafNode
from src.markdown import extract_markdown_images, extract_markdown_links


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


def text_node_to_html_node(text_node: "TextNode") -> LeafNode:
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
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextTypes.TEXT.value:
            # we only split TextNodes of type text
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid Markdown, wrong number of delimiters: {delimiter}")

        split_nodes: list[TextNode] = []
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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextTypes.TEXT.value:
            # we only split TextNodes of type text
            new_nodes.append(old_node)
            continue

        text_to_process: str = old_node.text
        images = extract_markdown_images(text_to_process)
        split_nodes: list[TextNode] = []
        for alt, url in images:
            split = text_to_process.split(f"![{alt}]({url})", maxsplit=1)
            if len(split) == 0:
                raise ValueError("Image not found")

            split_nodes.append(TextNode(split[0], TextTypes.TEXT))
            split_nodes.append(TextNode(alt, TextTypes.IMAGE, url))

            if len(split) == 2:
                text_to_process = split[1]

        if text_to_process:
            split_nodes.append(TextNode(text_to_process, TextTypes.TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextTypes.TEXT.value:
            # we only split TextNodes of type text
            new_nodes.append(old_node)
            continue

        text_to_process: str = old_node.text
        links = extract_markdown_links(text_to_process)
        split_nodes: list[TextNode] = []
        for anchor, url in links:
            split = text_to_process.split(f"[{anchor}]({url})", maxsplit=1)
            if len(split) == 0:
                raise ValueError("Link not found")

            split_nodes.append(TextNode(split[0], TextTypes.TEXT))
            split_nodes.append(TextNode(anchor, TextTypes.LINK, url))

            if len(split) == 2:
                text_to_process = split[1]

        if text_to_process:
            split_nodes.append(TextNode(text_to_process, TextTypes.TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes


def markdown_text_to_textNodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextTypes.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextTypes.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextTypes.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextTypes.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
