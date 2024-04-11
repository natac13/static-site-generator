import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        actual = extract_markdown_images(text)
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertListEqual(expected, actual)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        actual = extract_markdown_images(text)
        expected = []
        self.assertListEqual(expected, actual)

    def test_extract_markdown_images_one_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        actual = extract_markdown_images(text)
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            )
        ]
        self.assertListEqual(expected, actual)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        actual = extract_markdown_links(text)
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(expected, actual)

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        actual = extract_markdown_links(text)
        expected = []
        self.assertEqual(expected, actual)

    def test_extract_markdown_links_one_link(self):
        text = "This is text with a [link](https://www.example.com)"
        actual = extract_markdown_links(text)
        expected = [("link", "https://www.example.com")]
        self.assertEqual(expected, actual)

    def test_split_nodes_images(self):

        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        actual = split_nodes_images([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(expected, actual)

    def test_split_nodes_images_no_images(self):
        node = TextNode("This is text with no images", text_type_text)
        actual = split_nodes_images([node])
        expected = [node]
        self.assertEqual(expected, actual)

    def test_split_nodes_images_one_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text,
        )
        actual = split_nodes_images([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
        ]
        self.assertEqual(expected, actual)

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
            text_type_text,
        )
        actual = split_nodes_links([node])
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://www.example.com",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second link",
                text_type_link,
                "https://www.example.com/another",
            ),
        ]
        self.assertEqual(expected, actual)

    def test_split_nodes_links_no_links(self):
        node = TextNode("This is text with no links", text_type_text)
        actual = split_nodes_links([node])
        expected = [node]
        self.assertEqual(expected, actual)

    def test_split_nodes_links_one_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)", text_type_text
        )
        actual = split_nodes_links([node])
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://www.example.com",
            ),
        ]
        self.assertEqual(expected, actual)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        for i, node in enumerate(actual):
            print(i, node)
        self.assertEqual(expected, actual)

    def test_text_to_textnodes_extreme(self):
        text = """This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev) and **another bold** and *another italic* and `another code` and ![another image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another link](https://boot.dev)"""
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("another bold", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("another italic", text_type_italic),
            TextNode(" and ", text_type_text),
            TextNode("another code", text_type_code),
            TextNode(" and ", text_type_text),
            TextNode(
                "another image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and ", text_type_text),
            TextNode("another link", text_type_link, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
