import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        node = HTMLNode(None, None, None, props)
        self.assertEqual(
            'href="https://www.google.com" target="_blank"',
            node.props_to_html()
        )

    def test_props_to_html_noprops(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual("", node.props_to_html())

    def test__repr__(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        node = HTMLNode("tag", None, None, props)
        self.assertEqual(
            "HTMLNode(tag, None, None, {'href': 'https://www.google.com', 'target': '_blank'})",
            repr(node)
        )


if __name__ == "__main__":
    unittest.main()
