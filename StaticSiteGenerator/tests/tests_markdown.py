import unittest

from src.markdown import extract_markdown_images, extract_markdown_links


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
