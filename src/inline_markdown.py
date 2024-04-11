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
        original_text = old_node.text
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            delimiter = f"![{image[0]}]({image[1]})"
            sections = original_text.split(delimiter, 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            before = sections[0]
            if before != "":
                new_nodes.append(TextNode(before, text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            links = original_text.split(delimiter, 1)
            before = links[0]
            if before != "":
                new_nodes.append(TextNode(before, text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = links[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def text_to_textnodes(text: str):
    """
    Takes raw text and returns a list of TextNode objects.
    """
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes
