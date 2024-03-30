# test the html node class

import unittest
from htmlnode import HTMLNode
from textnode import TextNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(
            tag="div",
            value="Hello",
            children=[HTMLNode(tag="p", value="World")],
            props={"class": "container"},
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].value, "World")
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html(self):
        node = HTMLNode(props={"class": "container", "id": "main"})
        props_html = node.props_to_html()
        self.assertEqual(props_html, ' class="container" id="main"')

    def test_repr(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        self.assertEqual(
            str(node),
            "HTMLNode(tag: div, value: None, children: [], props: {'class': 'container'})",
        )

    def test_text_node_to_html_text(self):
        text_node = TextNode("Hello", "text")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.children, [])

    def test_text_node_to_html_bold(self):
        text_node = TextNode("Hello", "bold")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.children, [])

    def test_text_node_to_html_italic(self):
        text_node = TextNode("Hello", "italic")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.children, [])

    def test_text_node_to_html_code(self):
        text_node = TextNode("Hello", "code")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.children, [])

    def test_text_node_to_html_link(self):
        text_node = TextNode("Hello", "link", "https://www.boot.dev")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        self.assertEqual(html_node.children, [])

    def test_text_node_to_html_image(self):
        text_node = TextNode("Hello", "image", "https://www.boot.dev")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://www.boot.dev", "alt": "Hello"}
        )
        self.assertEqual(html_node.children, [])

    def test_text_node_to_html_invalid(self):
        try:
            text_node = TextNode("Hello", "invalid")
            HTMLNode.text_node_to_html_node(text_node)
            assert False, "Expected ValueError to be raised"
        except ValueError as e:
            assert str(e) == "Invalid text node type"


if __name__ == "__main__":
    unittest.main()
