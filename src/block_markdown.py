import re


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
    print(block)

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
