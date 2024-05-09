import unittest

from src.markdownBlock import BlockTypes, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple(self):
        markdown = """# two liner
text"""
        expected = ["# two liner\ntext"]
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, expected)

    def test_strip(self):
        markdown = """ # two liner
text               """
        expected = ["# two liner\ntext"]
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, expected)

    def test_excessive_newline(self):
        markdown = """# two liner





text"""
        expected = ["# two liner", "text"]
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, expected)

    def test_multiple(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        expected = [
            "This is **bolded** paragraph",
            """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
            """* This is a list
* with items""",
        ]
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        markdown = """text"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.PARAGRAPH)

    def test_paragraph2(self):
        markdown = """*text"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.PARAGRAPH)

    def test_heading(self):
        markdown = """# text"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.HEADING)

    def test_heading(self):
        markdown = """###### text"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.HEADING)

    def test_non_heading(self):
        markdown = """####### text"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.PARAGRAPH)

    def test_non_heading2(self):
        markdown = """#text"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.PARAGRAPH)

    def test_codeblock(self):
        markdown = """```
        #text
```"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.CODE)

    def test_quote(self):
        markdown = """>text
>text2
>text3"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.QUOTE)

    def test_ulist(self):
        markdown = """- text
- text2
- text3"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.UNORDERED_LIST)

    def test_ulist2(self):
        markdown = """* text
* text2
* text3"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.UNORDERED_LIST)

    def test_not_ulist(self):
        markdown = """*text
-text2
*text3"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.PARAGRAPH)

    def test_not_ulist2(self):
        markdown = """-text
- text2"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.PARAGRAPH)

    def test_olist(self):
        markdown = """1. text
2. text2
3. text3
4. hi
5. hi
6. hi
7. hi
8. hi
9. hi
10. hi
11. 1"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.ORDERED_LIST)

    def test_not_olist(self):
        markdown = """1. text
2. text2
3. text3
5. hi
5. hi
6. hi"""
        blocks = markdown_to_blocks(markdown)
        block_type = block_to_block_type(blocks[0])

        self.assertEqual(block_type, BlockTypes.PARAGRAPH)
