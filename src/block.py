from enum import Enum
import re

from leafnode import LeafNode
from node_util import text_to_textnodes, textnode_to_htmlnode
from parentnode import ParentNode


heading_regex = "^#+ "
unordered_list_regex = "^[*-] "
quote_regex = "^[>] "
ordered_list_regex = "^\\d+\\. "
code_identifier = "```"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def append_line_to_last_list_item(lst, line):
    lst.append(f"{lst.pop()}\n{line}")

def markdown_to_blocks(markdown):
    blocks = []
    prev_block_type = None
    for line in markdown.split("\n"):
        line = line.strip()

        if len(line) == 0:
            prev_block_type = None
            continue

        if re.match(code_identifier, line) or prev_block_type == BlockType.CODE:
            if prev_block_type == BlockType.CODE:
                append_line_to_last_list_item(blocks, line)
                if re.match(code_identifier, line):
                    prev_block_type = None
            else:
                prev_block_type = BlockType.CODE
                blocks.append(line)
            continue

        # Assume headings and paragraphs are single line
        continue_block = False
        if (re.match(unordered_list_regex, line) and prev_block_type == BlockType.UNORDERED_LIST) or \
            (re.match(ordered_list_regex, line) and prev_block_type == BlockType.ORDERED_LIST) or \
            (re.match(quote_regex, line) and prev_block_type == BlockType.QUOTE):
            continue_block = True
        else:
            blocks.append(line)

        if continue_block:
            append_line_to_last_list_item(blocks, line)

        prev_block_type = block_to_block_type(blocks[-1])

    return blocks

def lines_match(lines, regex):
    for line in lines.split("\n"):
        if not re.match(regex, line):
            return False
    return True


def block_to_block_type(markdown_block):
    if re.match(heading_regex, markdown_block):
        return BlockType.HEADING

    if markdown_block.startswith(code_identifier) and markdown_block.endswith(code_identifier):
        return BlockType.CODE

    if re.match(quote_regex, markdown_block):
        return BlockType.QUOTE

    if re.match(unordered_list_regex, markdown_block):
        return BlockType.UNORDERED_LIST

    if re.match(ordered_list_regex, markdown_block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def remove_markdown_regex(block, regex):
    new_block = ""
    for line in block.splitlines():
        new_block += re.sub(regex, "", line) + "\n"
    return new_block[:-1]

def markdown_to_html_node(markdown):
    nodes = []

    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                count = block.count("#")
                block = remove_markdown_regex(block, heading_regex)
                leaves = map(textnode_to_htmlnode, text_to_textnodes(block))
                nodes.append(ParentNode(f"h{count}", leaves))
            case BlockType.PARAGRAPH:
                leaves = map(textnode_to_htmlnode, text_to_textnodes(block))
                nodes.append(ParentNode("p", leaves))
            case BlockType.CODE:
                block = remove_markdown_regex(block, code_identifier)
                block = "".join(block.splitlines()[1:])
                code = LeafNode("code", block)
                nodes.append(code)
            case BlockType.QUOTE:
                block = remove_markdown_regex(block, quote_regex)
                node = LeafNode("blockquote", block)
                nodes.append(node)
            case BlockType.UNORDERED_LIST:
                block = remove_markdown_regex(block, unordered_list_regex)
                node = "".join(map(lambda l: LeafNode("li", l).to_html(), block.split("\n")))
                node = map(textnode_to_htmlnode, text_to_textnodes(node))
                nodes.append(ParentNode("ul", node))
            case BlockType.ORDERED_LIST:
                block = remove_markdown_regex(block, ordered_list_regex)
                node = "".join(map(lambda l: LeafNode("li", l).to_html(), block.split("\n")))
                node = map(textnode_to_htmlnode, text_to_textnodes(node))
                nodes.append(ParentNode("ol", node))

    return ParentNode("div", nodes)
