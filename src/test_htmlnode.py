import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_props_to_html(self):
        node = HTMLNode("p", "another value", None, {"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(result, string)

    def test_repr(self):
        node = HTMLNode("h", "last value", None, {"one": "two"})
        result = repr(node)
        string = "tag=h, value=last value, children=None, props={'one': 'two'}"
        self.assertEqual(result, string)

if __name__ == "__main__":
    unittest.main()