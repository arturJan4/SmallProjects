import unittest

from src.markdownText import (extract_markdown_images, extract_markdown_links,
                              markdown_text_to_textNodes,
                              split_nodes_delimiter, split_nodes_image,
                              split_nodes_link)
from src.textNode import TextNode, TextTypes


class TestExtractingFromMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](example.png)."
        actual = extract_markdown_images(text)
        expected = [("image", "example.png")]

        self.assertEqual(actual, expected)

    def test_extract_markdown_images_none(self):
        text = "This is text with an with no image."
        actual = extract_markdown_images(text)
        expected = []

        self.assertEqual(actual, expected)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with an ![image](example.png) and another one ![another](another.site.png) here."
        actual = extract_markdown_images(text)
        expected = [("image", "example.png"), ("another", "another.site.png")]

        self.assertEqual(actual, expected)

    def test_extract_markdown_images_none_tricky(self):
        text = "This is text with an with no ![image]."
        actual = extract_markdown_images(text)
        expected = []

        self.assertEqual(actual, expected)

    def test_extract_markdown_images_none_tricky2(self):
        text = "This is text with an with no (image.jpg)."
        actual = extract_markdown_images(text)
        expected = []

        self.assertEqual(actual, expected)

    def test_extract_markdown_links(self):
        text = "This is text with an [link text](example.com)."
        actual = extract_markdown_links(text)
        expected = [("link text", "example.com")]

        self.assertEqual(actual, expected)

    def test_extract_markdown_links_only(self):
        text = "[link text](/)."
        actual = extract_markdown_links(text)
        expected = [("link text", "/")]

        self.assertEqual(actual, expected)

    def test_extract_markdown_links_none(self):
        text = "This is text with an no links."
        actual = extract_markdown_links(text)
        expected = []

        self.assertEqual(actual, expected)

    def test_extract_markdown_links_none_tricky(self):
        text = "This is text with an no [links]."
        actual = extract_markdown_links(text)
        expected = []

        self.assertEqual(actual, expected)

    def test_extract_markdown_links_none_tricky2(self):
        text = "This is text with an no (links)."
        actual = extract_markdown_links(text)
        expected = []

        self.assertEqual(actual, expected)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with an [link text](example.com) and [another](site.example.org) one here."
        actual = extract_markdown_links(text)
        expected = [("link text", "example.com"), ("another", "site.example.org")]

        self.assertEqual(actual, expected)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("test", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)

        expected = [
            TextNode("test", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bad_type(self):
        node = TextNode("test", TextTypes.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)

        expected = [
            TextNode("test", TextTypes.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bad_and_correct_type(self):
        node = TextNode("wrong", TextTypes.CODE)
        node2 = TextNode("**test**", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextTypes.BOLD)

        expected = [TextNode("wrong", TextTypes.CODE), TextNode("test", TextTypes.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_whole(self):
        node = TextNode("**test**", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)

        expected = [
            TextNode("test", TextTypes.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple(self):
        node = TextNode("normal **test** more **bold**", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)

        expected = [
            TextNode("normal ", TextTypes.TEXT),
            TextNode("test", TextTypes.BOLD),
            TextNode(" more ", TextTypes.TEXT),
            TextNode("bold", TextTypes.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode("This is text with a *italic* word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextTypes.ITALIC)

        expected = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("italic", TextTypes.ITALIC),
            TextNode(" word", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.CODE)

        expected = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" word", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_uneven_delimiters_errors(self):
        with self.assertRaises(ValueError):
            node = TextNode("**test", TextTypes.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)

    def test_uneven_delimiters_errors_bigger(self):
        with self.assertRaises(ValueError):
            node = TextNode("--  **test . ", TextTypes.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)


class TestSplitNodesImages(unittest.TestCase):
    def test_no_image(self):
        node = TextNode(
            "This is text.",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [node]

        self.assertEqual(new_nodes, expected)

    def test_simple(self):
        node = TextNode(
            "This is text with an ![image](example.png).",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextTypes.TEXT),
            TextNode("image", TextTypes.IMAGE, "example.png"),
            TextNode(".", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple(self):
        txt = "This is text with an ![image](example.png) and another one ![another](another.site.png) here."
        node = TextNode(txt, TextTypes.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextTypes.TEXT),
            TextNode("image", TextTypes.IMAGE, "example.png"),
            TextNode(" and another one ", TextTypes.TEXT),
            TextNode("another", TextTypes.IMAGE, "another.site.png"),
            TextNode(" here.", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesLinks(unittest.TestCase):
    def test_no_link(self):
        node = TextNode(
            "This is text.",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [node]

        self.assertEqual(new_nodes, expected)

    def test_linkonly(self):
        node = TextNode(
            "[Home](/)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Home", TextTypes.LINK, "/"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_simple(self):
        node = TextNode(
            "This is text with an [link](example.png).",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", TextTypes.TEXT),
            TextNode("link", TextTypes.LINK, "example.png"),
            TextNode(".", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple(self):
        txt = "This is text with an [link](example.png) and another one [another link](another.site.png) here."
        node = TextNode(txt, TextTypes.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", TextTypes.TEXT),
            TextNode("link", TextTypes.LINK, "example.png"),
            TextNode(" and another one ", TextTypes.TEXT),
            TextNode("another link", TextTypes.LINK, "another.site.png"),
            TextNode(" here.", TextTypes.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestMarkdownTextToTextNodes(unittest.TestCase):
    def test_nothing(self):
        nodes = markdown_text_to_textNodes("")
        expected = []
        self.assertEqual(nodes, expected)

    def test_simple(self):
        nodes = markdown_text_to_textNodes("**bolded**")
        expected = [TextNode("bolded", TextTypes.BOLD)]
        self.assertEqual(nodes, expected)

    def test_simple_multiline(self):
        nodes = markdown_text_to_textNodes(
            """**bolded**
nonbolded"""
        )
        expected = [TextNode("bolded", TextTypes.BOLD), TextNode("\nnonbolded", TextTypes.TEXT)]
        self.assertEqual(nodes, expected)

    def test_simple_chain(self):
        nodes = markdown_text_to_textNodes("**bolded** and *italic*")
        expected = [
            TextNode("bolded", TextTypes.BOLD),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("italic", TextTypes.ITALIC),
        ]
        self.assertEqual(nodes, expected)

    def test_all_chain(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![cute image](https://th.bing.com/th/id/OIP.O21O10UUMdtcI_BsMbZQ_wHaHv) and a [link](example.org)."
        nodes = markdown_text_to_textNodes(text)
        expected = [
            TextNode("This is ", TextTypes.TEXT),
            TextNode("text", TextTypes.BOLD),
            TextNode(" with an ", TextTypes.TEXT),
            TextNode("italic", TextTypes.ITALIC),
            TextNode(" word and a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" and an ", TextTypes.TEXT),
            TextNode("cute image", TextTypes.IMAGE, "https://th.bing.com/th/id/OIP.O21O10UUMdtcI_BsMbZQ_wHaHv"),
            TextNode(" and a ", TextTypes.TEXT),
            TextNode("link", TextTypes.LINK, "example.org"),
            TextNode(".", TextTypes.TEXT),
        ]
        self.assertEqual(nodes, expected)
