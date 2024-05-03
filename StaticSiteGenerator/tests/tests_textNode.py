import unittest

from src.textNode import TextNode


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


if __name__ == "__main__":
    unittest.main()