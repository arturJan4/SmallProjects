import unittest

from src.HTMLNode import HTMLNode, LeafNode, ParentNode
from src.markdown import markdown_to_html, paragraph_to_html


class TestMarkdownToHTML(unittest.TestCase):
    def test_simple(self):
        self.fail()

    def test_paragraph(self):
        block = "hello\nworld"
        html = paragraph_to_html(block)

        children = [LeafNode(None, "hello\nworld", None)]
        expected = ParentNode(children, tag="p")

        self.assertEqual(html, expected)
