# test the html node class

import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
