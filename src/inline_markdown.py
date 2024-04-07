import re

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
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


def extract_markdown_images(text):
    """
    Takes raw text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images.
    """
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    """
    Takes raw text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images.
    """
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        image_matches = extract_markdown_images(old_node.text)
        split_nodes = []
        after = old_node.text
        for match in image_matches:
            delimiter = f"![{match[0]}]({match[1]})"
            sections = after.split(delimiter, 1)
            before = sections[0]
            if before != "":
                split_nodes.append(TextNode(before, text_type_text))
            split_nodes.append(TextNode(match[0], text_type_image, match[1]))
            if len(sections) == 1:
                break
            after = sections[1]

        if len(split_nodes) == 0:
            new_nodes.append(old_node)
            continue
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        link_matches = extract_markdown_links(old_node.text)
        split_nodes = []
        after = old_node.text
        for match in link_matches:
            delimiter = f"[{match[0]}]({match[1]})"
            sections = after.split(delimiter, 1)
            before = sections[0]
            if before != "":
                split_nodes.append(TextNode(before, text_type_text))
            split_nodes.append(TextNode(match[0], text_type_link, match[1]))
            if len(sections) == 1:
                break
            after = sections[1]

        if len(split_nodes) == 0:
            new_nodes.append(old_node)
            continue
        new_nodes.extend(split_nodes)
    return new_nodes
