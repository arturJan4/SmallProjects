from src.HTMLNode import HTMLNode, ParentNode
from src.markdownBlock import BlockTypes, block_to_block_type, markdown_to_blocks
from src.markdownText import TextNode, TextTypes, markdown_text_to_textNodes
from src.textNode import text_node_to_html_node


def markdown_to_html(markdown) -> HTMLNode:
    """
    HTML is rendered as a big div with children inside being blocks.
    Each Block is rendered as a list of children with associated tag.
    """
    blocks = markdown_to_blocks(markdown)

    block_to_HTML_functions = {
        BlockTypes.PARAGRAPH: paragraph_to_html,
        BlockTypes.QUOTE: quoteblock_to_html,
        BlockTypes.CODE: codeblock_to_html,
        BlockTypes.HEADING: heading_to_html,
        BlockTypes.UNORDERED_LIST: unordered_list_to_html,
        BlockTypes.ORDERED_LIST: ordered_list_to_html,
    }

    div_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type in block_to_HTML_functions:
            div_children.append(block_to_HTML_functions[block_type](block))
        else:
            raise NotImplementedError(f"{block_type} type not supported in conversion to HTML")

    return ParentNode(div_children, "div", None)


def paragraph_to_html(block: str) -> HTMLNode:
    children = []
    text_nodes = markdown_text_to_textNodes(block)

    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return ParentNode(children, "p", None)


def quoteblock_to_html(block: str) -> HTMLNode:
    """Identified by > at start of every line"""
    children = []

    # remove starting '>'
    block = "\n".join(map(lambda x: x[1:], block.split("\n")))

    text_nodes = markdown_text_to_textNodes(block)

    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return ParentNode(children, "blockquote", None)


def codeblock_to_html(block: str) -> HTMLNode:
    """Identified by ``` at start and end. Treat inside as a text"""
    code_node = TextNode(block[3:-3], TextTypes.TEXT)
    html_node = text_node_to_html_node(code_node)

    return ParentNode([html_node], "code", None)


def heading_to_html(block: str) -> HTMLNode:
    hashes, block = block.split(" ", maxsplit=1)
    strength = hashes.count("#")
    text_nodes = markdown_text_to_textNodes(block)

    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return ParentNode(children, f"h{strength}", None)


def unordered_list_to_html(block: str) -> HTMLNode:
    """Each item should be enclosed in li tag"""
    children = []

    lines = list(map(lambda x: x[2:], block.splitlines()))

    for line in lines:
        text_nodes = markdown_text_to_textNodes(line)

        li_children = []
        for text_node in text_nodes:
            li_children.append(text_node_to_html_node(text_node))

        list_element = ParentNode(li_children, "li", None)
        children.append(list_element)

    return ParentNode(children, "ul", None)


def ordered_list_to_html(block: str) -> HTMLNode:
    """Each item should be enclosed in li tag"""
    children = []

    lines = list(map(lambda x: x[2:], block.splitlines()))

    for line in lines:
        text_nodes = markdown_text_to_textNodes(line)

        li_children = []
        for text_node in text_nodes:
            li_children.append(text_node_to_html_node(text_node))

        list_element = ParentNode(li_children, "li", None)
        children.append(list_element)

    return ParentNode(children, "ol", None)
