import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})

    def test_tag_empty(self):
        node = HTMLNode(tag="")
    def test_value_empty(self):
        node = HTMLNode(value="")
    def test_children_empty(self):
        node = HTMLNode(children=[])
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "BOLD")
        self.assertEqual(node.to_html(), "<b>BOLD</b>")
    def test_leaf_to_html_i(self):
        node = LeafNode("i", "italic")
        self.assertEqual(node.to_html(), "<i>italic</i>")

       

if __name__ == "__main__":
    unittest.main()
