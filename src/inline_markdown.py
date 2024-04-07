import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


# r"!\[(.*?)\]\((.*?)\)"


def extract_markdown_images(text):
    """
    Takes raw text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images.
    """

    image_nodes = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        image_nodes.append((match[0], match[1]))

    return image_nodes


def extract_markdown_links(text):
    """
    Takes raw text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images.
    """

    image_nodes = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        image_nodes.append((match[0], match[1]))

    return image_nodes
