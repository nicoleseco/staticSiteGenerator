import unittest

from htmlnode import *
from text_to_html import *


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
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("this is bold", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "this is bold")

    #def test_text_to_img(self):
    #    node = TextNode("alt text", TextType.IMG_TEXT, "http://example.com/image.png")
     #   html_node = text_node_to_html_node(node)
      #  self.assertEqual(html_node.tag, 'img')
       # self.assertEqual(html_node.value, "")  # Image tags have empty value
        #self.assertEqual(html_node.props, {'src': "http://example.com/image.png", 'alt': "alt text"})

class TestSplitNodesDelimiter(unittest.TestCase):
    # Helper function to quickly create TextNode objects
    def create_text_node(self, value, text_type):
        return TextNode(value, text_type)

    def test_simple_matching_delimiter(self):
        # Case: A single node with a well-paired delimiter
        node = self.create_text_node("This is `code` in text", TextType.NORMAL_TYPE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        
        # Assert there are 3 resulting nodes
        self.assertEqual(len(new_nodes), 3)

        # Assert the first segment is regular text
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TYPE)

        # Assert the second segment is the delimited text
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)

        # Assert the third segment is regular text
        self.assertEqual(new_nodes[2].text, " in text")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL_TYPE)

    def test_no_delimiter_present(self):
        # Case: No delimiter in the text, should return original node
        node = self.create_text_node("This is plain text", TextType.NORMAL_TYPE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        
        # Assert the output contains the single original node
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TYPE)
      

if __name__ == "__main__":
    unittest.main()
