import unittest
from markdown_to_textnode import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes, 
    markdown_to_blocks, 
    block_to_block_type
) 
from textnode import TextNode, TextType, BlockType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images("This is text with an ![lol no picture](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("lol no picture", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images3(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgurallery.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgurallery.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images4(self):
        matches = extract_markdown_images("This is text with an ![image](http://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "http://i.imgur.com/zjjcJKZ.png")], matches)



    def test_extract_markdown_images(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.de) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.de"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](htps://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "htps://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links3(self):
        matches = extract_markdown_links("This is text with a link [to booot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to booot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links4(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youube", "https://www.youtube.com/@bootdotdev")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )


    def text_to_textnodes(self):
        text_nodes = text_to_textnodes('This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)')
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes,
        )


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks(self):
        block = '####kasjdfoaiwue'
        type = block_to_block_type(block)
        self.assertEqual(
            type, 
            BlockType.HEADING
        )

    def test_markdown_to_blocks2(self):
        block = '```ashdflkuhd```'
        type = block_to_block_type(block)
        self.assertEqual(
            type, 
            BlockType.CODE
        )

    def test_markdown_to_blocks3(self):
        block = '>kasjdfoaiwue'
        type = block_to_block_type(block)
        self.assertEqual(
            type, 
            BlockType.QUOTE
        )

    def test_markdown_to_blocks4(self):
        block = '-kasjdfoaiwue'
        type = block_to_block_type(block)
        self.assertEqual(
            type, 
            BlockType.UNORDERED_LIST
        )

    def test_markdown_to_blocks5(self):
        block = '1.kasjdfoaiwue'
        type = block_to_block_type(block)
        self.assertEqual(
            type, 
            BlockType.ORDERED_LIST
        )

    def test_markdown_to_blocks6(self):
        block = 'kasjdfoaiwue'
        type = block_to_block_type(block)
        self.assertEqual(
            type, 
            BlockType.PARAGRAPH
        )




if __name__ == "__main__":
    unittest.main()
