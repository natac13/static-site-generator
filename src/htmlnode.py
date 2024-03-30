class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        attributes = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        if attributes:
            return f" {attributes}"
        return ""

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

    def text_node_to_html_node(text_node):
        if text_node.text_type == "text":
            return LeafNode(None, text_node.text, None)
        if text_node.text_type == "bold":
            return LeafNode("b", text_node.text, None)
        if text_node.text_type == "italic":
            return LeafNode("i", text_node.text, None)
        if text_node.text_type == "code":
            return LeafNode("code", text_node.text, None)
        if text_node.text_type == "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        if text_node.text_type == "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        raise ValueError("Invalid text node type")


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode value cannot be None")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if children is None:
            raise ValueError("ParentNode children cannot be None")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode children cannot be None")

        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
