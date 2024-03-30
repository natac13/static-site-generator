class TextNode:
    """
    Represents a text node in a static site.

    Attributes:
      text (str): The text content of the node.
      text_type (str): The type of the text content.
      url (str, optional): The URL associated with the text node.

    Methods:
      __eq__(other): Checks if two TextNode objects are equal.
      __repr__(): Returns a string representation of the TextNode object.
    """

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
