import re
from textnode import TextNode, TextType
from leafnode import LeafNode


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
        if len(news) < 3:
            new_nodes.append(TextNode(n.text, TextType.TEXT))
            continue
        if len(news) > 3:
            raise Exception("Weird number of split")
        new_nodes.append(TextNode(news[0], TextType.TEXT))
        new_nodes.append(TextNode(news[1], text_type))
        new_nodes.append(TextNode(news[2], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        text = n.text
        images = extract_markdown_images(text)
        for i in range(len(images)):
            image_text = f"![{images[i][0]}]({images[i][1]})"
            text_parts = text.split(image_text)
            new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            if i == len(images) - 1 and len(text_parts[1]) > 0:
                new_nodes.append(TextNode(text_parts[1], TextType.TEXT))
            text = text_parts[1]

    if len(new_nodes) == 0:
        return old_nodes

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        text = n.text
        images = extract_markdown_links(text)
        for i in range(len(images)):
            image_text = f"[{images[i][0]}]({images[i][1]})"
            text_parts = text.split(image_text)
            new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(images[i][0], TextType.LINK, images[i][1]))
            if i == len(images) - 1 and len(text_parts[1]) > 0:
                new_nodes.append(TextNode(text_parts[1], TextType.TEXT))
            text = text_parts[1]

    if len(new_nodes) == 0:
        return old_nodes

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)]\((.*?)\)", text)
