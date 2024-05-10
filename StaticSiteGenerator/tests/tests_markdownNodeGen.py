import unittest

from src.HTMLNode import LeafNode, ParentNode
from src.markdownNodeGen import (
    codeblock_to_html,
    heading_to_html,
    ordered_list_to_html,
    paragraph_to_html,
    quoteblock_to_html,
    unordered_list_to_html,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_simple(self):
        self.fail()


class TestMarkdownToHTMLUtils(unittest.TestCase):
    def test_paragraph(self):
        # Actual
        block = "hello\nworld"
        html = paragraph_to_html(block)

        # Expected
        children = [LeafNode(None, "hello\nworld", None)]
        expected = ParentNode(children, tag="p")

        self.assertEqual(html, expected)

    def test_paragraph_formatted(self):
        # Actual
        block = "he*ll*o\n**world**\n"
        html = paragraph_to_html(block)

        # Expected
        word = lambda x: LeafNode(None, x)
        italic_word = LeafNode("i", "ll")
        bold_word = LeafNode("b", "world")

        children = [word("he"), italic_word, word("o\n"), bold_word, word("\n")]
        expected = ParentNode(children, tag="p")

        # Assert
        self.assertEqual(html, expected)

    def test_quouteblock(self):
        # Actual
        block = """>this is a quote
>by a **really** smart
>*guy*"""
        html = quoteblock_to_html(block)

        # Expected
        children = [LeafNode(None, "this is a quote\nby a ")]
        children.append(LeafNode("b", "really"))
        children.append(LeafNode(None, " smart\n"))
        children.append(LeafNode("i", "guy"))
        expected = ParentNode(children, tag="blockquote")

        self.assertEqual(html, expected)

    def test_codeblock(self):
        # Actual
        code = """this is a code
>by a **really** smart
>*guy*"""
        block = f"```{code}```"
        html = codeblock_to_html(block)

        # Expected
        children = [LeafNode(None, code)]
        expected = ParentNode(children, tag="code")

        self.assertEqual(html, expected)

    def test_heading_h1(self):
        # Actual
        headings = "# "
        sample_text = """Heading test
more text in new lines
yes"""
        block = f"{headings}{sample_text}"
        html = heading_to_html(block)

        # Expected
        children = [LeafNode(None, sample_text)]
        expected = ParentNode(children, tag="h1")

        self.assertEqual(html, expected)

    def test_heading_h6(self):
        # Actual
        headings = "###### "
        sample_text = """Heading test
more text in new lines
yes"""
        block = f"{headings}{sample_text}"
        html = heading_to_html(block)

        # Expected
        children = [LeafNode(None, sample_text)]
        expected = ParentNode(children, tag="h6")

        self.assertEqual(html, expected)

    def test_unordered_list(self):
        # Actual
        elements = ["first", "second", "third"]
        unordered_elements = [f"* {elem}" for elem in elements]
        block = "\n".join(unordered_elements)

        html = unordered_list_to_html(block)

        # Expected
        children = [ParentNode([LeafNode(None, elem)], "li") for elem in elements]
        expected = ParentNode(children, tag="ul")

        self.assertEqual(html, expected)

    def test_ordered_list(self):
        # Actual
        elements = ["first", "second", "third"]
        unordered_elements = [f"{idx+1}.{elem}" for idx, elem in enumerate(elements)]
        block = "\n".join(unordered_elements)

        html = ordered_list_to_html(block)

        # Expected
        children = [ParentNode([LeafNode(None, elem)], "li") for elem in elements]
        expected = ParentNode(children, tag="ol")

        self.assertEqual(html, expected)
