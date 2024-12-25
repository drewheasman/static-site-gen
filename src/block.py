from enum import Enum
import re

from leafnode import LeafNode
from node_util import text_to_textnodes, textnode_to_htmlnode
from parentnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = []
    prev_line = ""
    for line in markdown.split("\n"):
        line = line.strip()

        if len(line) > 0:
            match line[0]:
                case "*":
                    if prev_line.startswith("*"):
                        blocks.append(f"{blocks.pop()}\n{line}")
                    else:
                        blocks.append(line)
                case _:
                    blocks.append(line)
        prev_line = line

    return blocks

def lines_match(lines, regex):
    for line in lines.split("\n"):
        if not re.match(regex, line):
            return False
    return True


def block_to_block_type(markdown_block):
    if markdown_block.startswith("# "):
        return BlockType.HEADING

    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE

    if lines_match(markdown_block, "^[>] "):
        return BlockType.QUOTE

    if lines_match(markdown_block, "^[*-] "):
        return BlockType.UNORDERED_LIST

    if lines_match(markdown_block, "^\\d+\\. "):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    nodes = []

    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                node = LeafNode("h1", block[2:])
                nodes.append(node)
            case BlockType.PARAGRAPH:
                leaves = map(textnode_to_htmlnode, text_to_textnodes(block))
                nodes.append(ParentNode("p", leaves))
            # Have to add code identification to markdown_to_blocks
            # case BlockType.CODE:
            #     code = LeafNode("code", "\n".join(block.split("\n")[1:-1]))
            #     print(code)
            #     nodes.append(code)
            case BlockType.QUOTE:
                node = LeafNode("q", block)
                nodes.append(node)
            case BlockType.UNORDERED_LIST:
                node = ParentNode("ul", map(lambda l: LeafNode("li", l[2:]), block.split("\n")))
                nodes.append(node)
            case BlockType.ORDERED_LIST:
                node = ParentNode("ol", map(lambda l: LeafNode("li", re.sub("^\\d+\\. ", "", l)), block.split("\n")))
                nodes.append(node)

    return ParentNode("div", nodes)
