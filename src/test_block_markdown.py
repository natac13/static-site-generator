import unittest

from block_markdown import (
    block_to_block_type,
    markdown_to_blocks,
    block_type_heading,
    block_type_code,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_block_markdown(self):
        incoming = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        actual = markdown_to_blocks(incoming)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]

        self.assertEqual(expected, actual)

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        heading2 = "## Heading 2"
        actual2 = block_to_block_type(heading2)
        expected2 = block_type_heading  # type: ignore
        self.assertEqual(expected2, actual2)

    def test_block_to_block_type_code(self):
        code = """```
console.log("hello world")
```"""
        actual = block_to_block_type(code)
        self.assertEqual(block_type_code, actual)

    def test_block_to_block_type_quote(self):
        quote = "> This is a quote"
        actual = block_to_block_type(quote)
        self.assertEqual(block_type_quote, actual)

    def test_block_to_block_type_quote_multiline(self):
        quote = "> This is a quote\n> with multiple lines"
        actual = block_to_block_type(quote)
        self.assertEqual(block_type_quote, actual)

    def test_block_to_block_type_not_quote(self):
        not_quote = "> This is not a quote\nwith multiple lines"
        actual = block_to_block_type(not_quote)
        self.assertEqual(block_type_paragraph, actual)

    def test_block_to_block_type_unordered_list(self):
        unordered_list = "* This is a list\n* with items"
        actual = block_to_block_type(unordered_list)
        self.assertEqual(block_type_unordered_list, actual)

    def test_block_to_block_type_not_unordered_list(self):
        not_unordered_list = "* This is a list\nwith items"
        actual = block_to_block_type(not_unordered_list)
        self.assertEqual(block_type_paragraph, actual)

    def test_block_to_block_type_ordered_list(self):
        ordered_list = "1. This is a list\n2. with items"
        actual = block_to_block_type(ordered_list)
        self.assertEqual(block_type_ordered_list, actual)

    def test_block_to_block_type_not_ordered_list(self):
        not_ordered_list = "1. This is a list\nwith items"
        actual = block_to_block_type(not_ordered_list)
        self.assertEqual(block_type_paragraph, actual)

    def test_block_to_block_type_paragraph(self):
        paragraph = "This is a paragraph"
        actual = block_to_block_type(paragraph)
        self.assertEqual(block_type_paragraph, actual)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)


if __name__ == "__main__":
    unittest.main()
