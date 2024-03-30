import unittest
from leafNode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leafNode_to_html(self):
        leaf_node = LeafNode("p", "Hello, World!", {"class": "my-class"})
        expected_html = '<p class="my-class">Hello, World!</p>'
        self.assertEqual(leaf_node.to_html(), expected_html)

    def test_leafNode_to_html_no_tag(self):
        leaf_node = LeafNode(value="Hello, World!")
        expected_html = "Hello, World!"
        self.assertEqual(leaf_node.to_html(), expected_html)

    def test_leafNode_value_none(self):
        try:
            leaf_node = LeafNode()
            leaf_node.to_html()
            assert False, "Expected ValueError to be raised"
        except ValueError as e:
            assert str(e) == "LeafNode value cannot be None"

    def test_leafNode_tag_none(self):
        leaf_node = LeafNode(value="Hello, World!")
        leaf_node.tag = None
        expected_html = "Hello, World!"
        self.assertEqual(leaf_node.to_html(), expected_html)

    def test_to_html_with_anchor_tag(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        expected_html = '<a href="https://www.example.com">Click me!</a>'
        self.assertEqual(leaf_node.to_html(), expected_html)

    def test_repr(self):
        leaf_node = LeafNode("p", "Hello, World!", {"class": "my-class"})
        self.assertEqual(
            str(leaf_node),
            "LeafNode(p, Hello, World!, {'class': 'my-class'})",
        )


if __name__ == "__main__":
    unittest.main()
