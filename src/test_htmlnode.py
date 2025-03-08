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
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_greatgrandkids(self):
        greatgrandchild = LeafNode("b", "greatgrandchild")
        grandchild_node = ParentNode("span", [greatgrandchild])
        child_node = ParentNode("p", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(), "<div><p><span><b>greatgrandchild</b></span></p></div>",
        ) 
       

if __name__ == "__main__":
    unittest.main()
