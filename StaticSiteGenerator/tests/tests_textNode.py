import unittest

from src.HTMLNode import LeafNode
from src.textNode import (
    TextNode,
    TextTypes,
    markdown_text_to_textNodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("a", "b", url="c")
        self.assertEqual(repr(node), "TextNode(a, b, c)")


class TestConvertTextToHTML(unittest.TestCase):
    def test_convert_html_normal(self):
        node = TextNode("text node", "text")
        expected = LeafNode(tag=None, value="text node")
        actual = text_node_to_html_node(node)
        self.assertEqual(actual, expected)

    def test_convert_html_bold(self):
        node = TextNode("text node", "bold")
        expected = LeafNode(tag="b", value="text node")
        actual = text_node_to_html_node(node)
        self.assertEqual(actual, expected)

    def test_convert_html_italic(self):
        node = TextNode("text node", "italic")
        expected = LeafNode(tag="i", value="text node")
        actual = text_node_to_html_node(node)
        self.assertEqual(actual, expected)

    def test_convert_html_code(self):
        node = TextNode("text node", "code")
        expected = LeafNode(tag="code", value="text node")
        actual = text_node_to_html_node(node)
        self.assertEqual(actual, expected)

    def test_convert_html_link(self):
        txt = "anchor text"
        url = "example.org"
        node = TextNode(text=txt, text_type="link", url=url)
        expected = LeafNode(tag="a", value=txt, props={"href": url})
        actual = text_node_to_html_node(node)
        self.assertEqual(actual, expected)

    def test_convert_html_image(self):
        alt_text = "picture description"
        src = "example.jpg"
        node = TextNode(text=alt_text, text_type="image", url=src)
        expected = LeafNode(tag="img", value="", props={"src": src, "alt": alt_text})
        actual = text_node_to_html_node(node)
        self.assertEqual(actual, expected)

    def test_convert_html_error(self):
        with self.assertRaises(ValueError):
            node = TextNode(text="", text_type="pdf")
            test = text_node_to_html_node(node)


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


if __name__ == "__main__":
    unittest.main()
