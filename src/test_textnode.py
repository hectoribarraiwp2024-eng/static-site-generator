import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("this is almost the same", TextType.ITALIC)
        node2 = TextNode("this is almost the same", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_2(self):
        node = TextNode("this should pass", TextType.CODE, "www.abc.com")
        node2 = TextNode("this should not pass", TextType.CODE, "www.abc.com")
        self.assertNotEqual(node, node2)

    def test_repr_eq(self):
        node = TextNode("this is content", TextType.BOLD, "lol")
        result = repr(node)
        string = "TextNode(this is content, bold, lol)"
        self.assertEqual(result, string)


if __name__ == "__main__":
    unittest.main()