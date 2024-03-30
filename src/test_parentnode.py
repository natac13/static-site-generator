import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_parentNode_to_html(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("p", "World")
        parent_node = ParentNode("div", [child1, child2], {"class": "my-class"})
        expected_html = '<div class="my-class"><p>Hello</p><p>World</p></div>'
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_parentNode_to_html_no_tag(self):
        try:
            child1 = LeafNode("p", "Hello")
            child2 = LeafNode("p", "World")
            parent_node = ParentNode(None, [child1, child2])
            parent_node.to_html()
            assert False, "Expected ValueError to be raised"
        except ValueError as e:
            assert str(e) == "ParentNode tag cannot be None"

    def test_parentNode_tag_none(self):
        try:
            child1 = LeafNode("p", "Hello")
            child2 = LeafNode("p", "World")
            parent_node = ParentNode(None, [child1, child2])
            parent_node.to_html()
            assert False, "Expected ValueError to be raised"
        except ValueError as e:
            assert str(e) == "ParentNode tag cannot be None"

    def test_parentNode_children_none(self):
        try:
            parent_node = ParentNode("div", None)
            parent_node.to_html()
            assert False, "Expected ValueError to be raised"
        except ValueError as e:
            assert str(e) == "ParentNode children cannot be None"

    def test_parentNode_children_empty(self):
        try:
            parent_node = ParentNode("div", [])
            parent_node.to_html()
            assert False, "Expected ValueError to be raised"
        except ValueError as e:
            assert str(e) == "ParentNode children cannot be None"

    def test_repr(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("p", "World")
        parent_node = ParentNode("div", [child1, child2], {"class": "my-class"})
        self.assertEqual(
            str(parent_node),
            "ParentNode(div, [LeafNode(p, Hello, {}), LeafNode(p, World, {})], {'class': 'my-class'})",
        )

    def test_nested_parents(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("p", "World")
        parent1 = ParentNode("div", [child1, child2], {"class": "my-class"})
        parent2 = ParentNode("div", [parent1], {"class": "my-class"})
        expected_html = '<div class="my-class"><div class="my-class"><p>Hello</p><p>World</p></div></div>'
        self.assertEqual(parent2.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
