import unittest

from src.HTMLNode import LeafNode
from src.textNode import TextNode, text_node_to_html_node


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
        expected = LeafNode(tag="strong", value="text node")
        actual = text_node_to_html_node(node)
        self.assertEqual(actual, expected)

    def test_convert_html_italic(self):
        node = TextNode("text node", "italic")
        expected = LeafNode(tag="em", value="text node")
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


if __name__ == "__main__":
    unittest.main()
