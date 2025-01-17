import re
from textnode import TextNode, TextType
from leafnode import LeafNode

def text_to_textnodes(text):
    new_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def textnode_to_htmlnode(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {
                    "src": text_node.url,
                    "alt": text_node.text
                }
            )
        case _:
            raise Exception("TextNode has invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0 or len(delimiter) == 0:
        raise Exception("Invalid split nodes params")

    new_nodes = []
    for n in old_nodes:
        news = n.text.split(delimiter)
        news = list(filter(None, news))
        if len(news) == 1:
            new_nodes.append(n)
            continue
        if len(news) == 2:
            new_nodes.append(TextNode(news[0], text_type))
            new_nodes.append(TextNode(news[1], n.text_type))
            continue
        i = 0
        while i < len(news):
            if i % 2 == 0:
                new_nodes.append(TextNode(news[i], n.text_type))
            else:
                new_nodes.append(TextNode(news[i], text_type))
            i += 1

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        text = n.text
        images = extract_markdown_images(text)

        if len(images) == 0:
            new_nodes.append(n)

        for i in range(len(images)):
            image_text = f"![{images[i][0]}]({images[i][1]})"
            text_parts = text.split(image_text)
            new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            if i == len(images) - 1 and len(text_parts[1]) > 0:
                new_nodes.append(TextNode(text_parts[1], TextType.TEXT))
            text = text_parts[1]

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        text = n.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(n)

        for i in range(len(links)):
            image_text = f"[{links[i][0]}]({links[i][1]})"
            text_parts = text.split(image_text)
            new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(links[i][0], TextType.LINK, links[i][1]))
            if i == len(links) - 1 and len(text_parts[1]) > 0:
                new_nodes.append(TextNode(text_parts[1], TextType.TEXT))
            text = text_parts[1]

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)]\((.*?)\)", text)
