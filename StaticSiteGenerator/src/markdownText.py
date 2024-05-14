import re

from src.textNode import TextNode, TextTypes


def markdown_text_to_textNodes(text: str) -> list[TextNode]:
    """
    Returns:
        list of TextNodes describing markdown text
    """
    nodes: list[TextNode] = [TextNode(text, TextTypes.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextTypes.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextTypes.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextTypes.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextTypes) -> list[TextNode]:
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

            if len(split[0]) > 0:
                split_nodes.append(TextNode(split[0], TextTypes.TEXT))
            split_nodes.append(TextNode(anchor, TextTypes.LINK, url))

            if len(split) == 2:
                text_to_process = split[1]

        if text_to_process:
            split_nodes.append(TextNode(text_to_process, TextTypes.TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Example:
        markdown image format is
        ![alt text](url)
        eg. ![image](example.jpg)

    Returns:
        list of tuples containing alt text and URL
    """
    pattern = r"!\[(.*?)\]\((.+?)\)"
    found = re.findall(pattern, text)
    return found


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Example:
        markdown link format is
        [anchor text](url)
        eg. [link](example.com)

    Returns:
        list of tuples containing anchor text and URL
    """
    pattern = r"(?!!)\[(.*?)\]\((.+?)\)"
    found = re.findall(pattern, text)
    return found
