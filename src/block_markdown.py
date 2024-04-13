def markdown_to_blocks(markdown: str):
    res = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block is None or block == "":
            continue
        trimmed = block.strip()
        res.append(trimmed)
    return res
