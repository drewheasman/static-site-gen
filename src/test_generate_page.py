
import unittest

from generate_page import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_extract_title(self):
        markdown_with_heading = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. This is the first item in an ordered list block
2. This is the second item in an ordered list block
3. This is the third item in an ordered list block

"""
        markdown_with_heading_2 = """

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# This is a heading

* This is the first list item in a list block
* This is a list item
* This is another list item

1. This is the first item in an ordered list block
2. This is the second item in an ordered list block
3. This is the third item in an ordered list block

"""

        markdown_no_heading = """This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. This is the first item in an ordered list block
2. This is the second item in an ordered list block
3. This is the third item in an ordered list block

"""

        self.assertEqual("This is a heading", extract_title(markdown_with_heading))
        self.assertEqual("This is a heading", extract_title(markdown_with_heading_2))
        self.assertRaises(Exception, extract_title, markdown_no_heading)
