import unittest

from src.parentNode import ParentNode
from src.leafNode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("h1", "text", {"class": "cl1"})
        node2 = LeafNode("h1", "text", {"class": "cl1"})

        pnode1 = ParentNode(children=[node, node2], tag="h1", props=None)
        pnode2 = ParentNode(children=[node, node2], tag="h1", props=None)

        self.assertEqual(pnode1, pnode2)

    def test_neq(self):
        node = LeafNode("h1", "text", {"class": "cl1"})
        node2 = LeafNode("h1", "text", {"class": "cl2"})

        pnode1 = ParentNode(children=[node, node2], tag="h1", props=None)
        pnode2 = ParentNode(children=[node, node], tag="h1", props=None)
        self.assertNotEqual(pnode1, pnode2)

    def test_to_html(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        actual = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(actual, expected)

    def test_to_html_multiple(self):
        node1 = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node2 = ParentNode(
            tag="h",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "\n"),
                ParentNode(
                    tag="h2",
                    children=[LeafNode(None, "hello "), LeafNode("b", "world!")],
                    props={"class": "test"},
                ),
                LeafNode(None, "\n"),
                LeafNode(None, "text2"),
            ],
        )

        node3 = ParentNode(
            tag="h1",
            children=[
                LeafNode(None, "txt"),
                LeafNode("a", "page", {"href": "example.com"}),
                LeafNode(None, "\n"),
                node2,
                LeafNode(None, "\n"),
                LeafNode("i", "txt"),
                LeafNode(None, "\n"),
                node1,
            ],
        )

        actual = node3.to_html()
        expected = """<h1>txt<a href="example.com">page</a>
<h><b>Bold text</b>
<h2 class="test">hello <b>world!</b></h2>
text2</h>
<i>txt</i>
<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></h1>"""
        self.assertEqual(actual, expected)

    def test_to_html_raises(self):
        no_children = ParentNode(children=None, tag="p")
        with self.assertRaises(ValueError):
            html = no_children.to_html()

        no_tag = ParentNode(children=[LeafNode("text")], tag=None)
        with self.assertRaises(ValueError):
            html = no_tag.to_html()


if __name__ == "__main__":
    unittest.main()
