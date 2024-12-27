import unittest

from block import BlockType, markdown_to_blocks, lines_match, block_to_block_type, markdown_to_html_node


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown_string = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. Here
2. is
3. an
4. ordered
5. list

```
Ma code
```

"""

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
            """1. Here
2. is
3. an
4. ordered
5. list""",
            """```
Ma code
```"""
        ]

        self.assertEqual(expected, markdown_to_blocks(markdown_string))

    def test_lines_match(self):
        empty_string = ""
        single_character = "*"
        single_line = "* this is my line"
        multiple_lines = """* this is my line
* this is my second line
* this is my third line"""
        multiple_lines_2 = """* this is my line
this is my second line
* this is my third line"""

        self.assertTrue(lines_match(single_line, "^[*] "))
        self.assertTrue(lines_match(multiple_lines, "^[*] "))

        self.assertFalse(lines_match(empty_string, "^[*] "))
        self.assertFalse(lines_match(single_character, "^[*] "))
        self.assertFalse(lines_match(single_line, "^[*][*] "))
        self.assertFalse(lines_match(multiple_lines, "^[*][*] "))
        self.assertFalse(lines_match(multiple_lines_2, "^[*][*] "))

    def test_block_to_block_type(self):
        header_block = "# This is a heading"
        paragraph_block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        unordered_list_block = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ordered_list_block = """1. This is the first list item in a list block
20. This is a list item
300. This is another list item"""
        quote_block = """> The first line of the quote
> The second line of the quote
> The third line of the quote"""
        code_block = """```
ls -l ~/
```"""

        self.assertEqual(BlockType.HEADING, block_to_block_type(header_block))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(paragraph_block))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered_list_block))
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(ordered_list_block))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote_block))
        self.assertEqual(BlockType.CODE, block_to_block_type(code_block))

    def test_markdown_to_html_node(self):
        markdown_string = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. Here
2. is
3. an
4. ordered
5. list

```
Ma code
```

> quote

"""

        expected_html = """<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><ol><li>Here</li><li>is</li><li>an</li><li>ordered</li><li>list</li></ol><code>Ma code</code><blockquote>quote</blockquote></div>"""

        html_nodes = markdown_to_html_node(markdown_string)

        self.assertEqual(expected_html, html_nodes.to_html())
