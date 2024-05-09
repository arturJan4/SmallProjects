import re
from enum import StrEnum, auto


class BlockTypes(StrEnum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


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
    pattern = r"[^!]\[(.*?)\]\((.+?)\)"
    found = re.findall(pattern, text)
    return found


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Args:
        markdown (str): raw multiline Markdown string

    Returns:
        list[str]: list of distinct blocks
    """

    # blocks are separated by a newline
    split = markdown.split("\n\n")
    # remove empty blocks
    non_empty = filter(lambda x: len(x.strip()) > 0, split)
    # remove leading and trailing whitespace
    blocks = list(map(lambda x: x.strip(), non_empty))
    return blocks


def block_to_block_type(markdown_block: str) -> BlockTypes:
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    heading_pattern = r"#{1,6} \w+"
    if re.match(heading_pattern, markdown_block):
        return BlockTypes.HEADING

    # Code blocks must start with 3 backticks and end with 3 backticks.
    if len(markdown_block) >= 6 and markdown_block[:3] == "```" and markdown_block[-3:] == "```":
        return BlockTypes.CODE

    # Every line in a quote block must start with a > character.
    lines = markdown_block.split("\n")
    if all([line.startswith(">") for line in lines]):
        return BlockTypes.QUOTE

    # Every line in an unordered list block must start with a * or - character, followed by a space.
    if all([line.startswith("* ") for line in lines]) or all([line.startswith("- ") for line in lines]):
        return BlockTypes.UNORDERED_LIST

    # Every line in an ordered list block must start with a number followed by a . character and a space.
    # The number must start at 1 and increment by 1 for each line.
    starting = 1
    ordered_list = True
    for line in lines:
        matched = f"{starting}. "
        if not line.startswith(matched):
            ordered_list = False
            break

        starting += 1
    if ordered_list:
        return BlockTypes.ORDERED_LIST

    return BlockTypes.PARAGRAPH
