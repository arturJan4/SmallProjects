from src.HTMLNode import HTMLNode, LeafNode, ParentNode
from src.markdownBlock import BlockTypes, block_to_block_type, markdown_to_blocks
from src.markdownText import markdown_text_to_textNodes
from src.textNode import text_node_to_html_node


def markdown_to_html(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    block_to_HTML_functions = {
        BlockTypes.PARAGRAPH: paragraph_to_html,
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
