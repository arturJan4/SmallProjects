import unittest

from src.HTMLNode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "text", None, {"class": "cl1"})
        node2 = HTMLNode("h1", "text", None, {"class": "cl1"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("h1", "text", None, {"class": "cl1"})
        node2 = HTMLNode("h1", "text", None, {"class": "cl2"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("a", "b", None, {"cl": "1"})
        self.assertEqual(repr(node), "HTMLNode(a, b, None, {'cl': '1'})")

    def test_props_to_html(self):
        node = HTMLNode("h1", "text", None, {"class": "cl1"})
        self.assertEqual(node.props_to_html(), 'class="cl1"')

        node = HTMLNode("h1", "text", None, 
                        {"class": "cl1 cl2", "target": "_blank"})
        self.assertEqual(node.props_to_html(),
                         'class="cl1 cl2" target="_blank"')


if __name__ == "__main__":
    unittest.main()
