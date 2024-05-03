import unittest

from src.leafNode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("h1", "text", {"class": "cl1"})
        node2 = LeafNode("h1", "text", {"class": "cl1"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = LeafNode("h1", "text", {"class": "cl1"})
        node2 = LeafNode("h1", "text", {"class": "cl2"})
        self.assertNotEqual(node, node2)

    def test_to_html(self):
        node = LeafNode("p", "text", {"class": "cl1"})
        self.assertEqual(node.to_html(), '<p class="cl1">text</p>')

        node = LeafNode("a", "Click me!",
                        {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),
                         '<a href="https://www.google.com">Click me!</a>')


if __name__ == "__main__":
    unittest.main()
