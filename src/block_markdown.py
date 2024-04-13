import re

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, text_type_text


def markdown_to_blocks(markdown: str):
    res = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block is None or block == "":
            continue
        trimmed = block.strip()
        res.append(trimmed)
    return res


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def block_to_block_type(block: str):
    """
    We will support 6 types of markdown blocks:

    "paragraph"
    "heading"
    "code"
    "quote"
    "unordered_list"
    "ordered_list
    """
    # print(block)

    if re.match(r"#{0,6} ", block) is not None:
        return block_type_heading
    if re.search(r"^`{3}\n.*\n`{3}$", block) is not None:
        return block_type_code
    if re.match(r"> ", block) is not None:
        # check every line
        lines = block.splitlines()
        is_quote = True
        for line in lines:
            if re.match(r"> ", line) is None:
                is_quote = False
        if is_quote:
            return block_type_quote
        return block_type_paragraph
    if re.match(r"[*|-] ", block) is not None:
        lines = block.splitlines()
        is_list = True
        for line in lines:
            if re.match(r"[*|-] ", line) is None:
                is_list = False
        if is_list:
            return block_type_unordered_list
        return block_type_paragraph
    if re.match(r"1\. ", block) is not None:
        lines = block.splitlines()
        is_list = True
        next_num = 1
        for line in lines:
            if re.match(rf"{next_num}\. ", line) is None:
                is_list = False
            next_num += 1
        if is_list:
            return block_type_ordered_list
        return block_type_paragraph
    else:
        return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
