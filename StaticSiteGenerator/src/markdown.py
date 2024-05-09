import re


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
    Example
        markdown link format is
        [anchor text](url)
        eg. [link](example.com)

    Returns:
        list of tuples containing anchor text and URL
    """
    pattern = r"[^!]\[(.*?)\]\((.+?)\)"
    found = re.findall(pattern, text)
    return found
