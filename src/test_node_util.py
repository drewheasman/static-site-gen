import unittest

from node_util import textnode_to_htmlnode, text_to_textnodes
from node_util import extract_markdown_images, extract_markdown_links
from node_util import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType
from leafnode import LeafNode


class TestConvert(unittest.TestCase):
    def test_textnode_to_htmlnode_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(
            LeafNode(None, "This is a text node"),
            textnode_to_htmlnode(text_node)
        )

    def test_textnode_to_htmlnode_bold(self):
        bold_node = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(
            LeafNode("b", "This is a bold node"),
            textnode_to_htmlnode(bold_node)
        )

    def test_textnode_to_htmlnode_italic(self):
        italic_node = TextNode("This is a italic node", TextType.ITALIC)
        self.assertEqual(
            LeafNode("i", "This is a italic node"),
            textnode_to_htmlnode(italic_node)
        )

    def test_textnode_to_htmlnode_code(self):
        code_node = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(
            LeafNode("code", "This is a code node"),
            textnode_to_htmlnode(code_node)
        )

    def test_textnode_to_htmlnode_link(self):
        link_node = TextNode(
            "This is a link node",
            TextType.LINK,
            "http://example.com"
        )
        self.assertEqual(
            LeafNode("a", "This is a link node", {"href": link_node.url}),
            textnode_to_htmlnode(link_node)
        )

    def test_textnode_to_htmlnode_img(self):
        image_node = TextNode(
            "This is an image node",
            TextType.IMAGE,
            "http://example.com"
        )
        self.assertEqual(
            LeafNode(
                "img",
                "",
                {
                    "src": image_node.url,
                    "alt": "This is an image node"
                }
            ),
            textnode_to_htmlnode(image_node)
        )

    def test_split_nodes_delimiter_text(self):
        node = TextNode("This is text with a text word", TextType.TEXT)
        self.assertRaises(
            Exception,
            split_nodes_delimiter,
            ([node], " ", TextType.TEXT)
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode(
            "This is text with a **bold block** word",
            TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_not_found(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
        ]
        self.assertEqual(expected_nodes, new_nodes)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                         ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))

    def test_extract_markdown_images_blank(self):
        text = ""
        self.assertEqual([], extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text *with* a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube",
                         "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))

    def test_extract_markdown_link_ignore_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([], extract_markdown_links(text))

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        new_nodes = split_nodes_image([node])

        self.assertEqual(expected_nodes, new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        new_nodes = split_nodes_link([node])

        self.assertEqual(expected_nodes, new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(expected, text_to_textnodes(text))



if __name__ == "__main__":
    unittest.main()
