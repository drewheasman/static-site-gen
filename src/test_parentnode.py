import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_one_level(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            node.to_html()
        )

    def test_to_html_two_levels(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("h3", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                ]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            "<p><b>Bold text</b><h3><b>Bold text</b>Normal text</h3><i>italic text</i>Normal text</p>",
            node.to_html()
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
            {
                "data-testid": "this",
                "title": "that"
            }
        )

        self.assertEqual(
            '<p data-testid="this" title="that"><b>Bold text</b>Normal text</p>',
            node.to_html()
        )


if __name__ == "__main__":
    unittest.main()
