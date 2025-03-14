import unittest

from htmlnode import *
from text_to_html import *
from markdown_regex import *


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
   #def create_text_node(self, value, text_type):
    #    return TextNode(value, text_type)

#    def test_simple_matching_delimiter(self):
        # Case: A single node with a well-paired delimiter
 #       node = self.create_text_node("This is `code` in text", TextType.NORMAL_TYPE)
  #      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
   #     
        # Assert there are 3 resulting nodes
#        self.assertEqual(len(new_nodes), 3)

        # Assert the first segment is regular text
 #       self.assertEqual(new_nodes[0].text, "This is ")
  #      self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TYPE)

        # Assert the second segment is the delimited text
   #     self.assertEqual(new_nodes[1].text, "code")
    #    self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)

        # Assert the third segment is regular text
     #   self.assertEqual(new_nodes[2].text, " in text")
      #  self.assertEqual(new_nodes[2].text_type, TextType.NORMAL_TYPE)

 #   def test_no_delimiter_present(self):
        # Case: No delimiter in the text, should return original node
  ##     new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        
        # Assert the output contains the single original node
    #    self.assertEqual(len(new_nodes), 1)
     #   self.assertEqual(new_nodes[0].text, "This is plain text")
      #  self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TYPE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TYPE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TYPE),
                TextNode("image", TextType.IMG_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TYPE),
                TextNode(
                    "second image", TextType.IMG_TEXT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        


    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://youtube.com) and another [second link](https://google.com)",
            TextType.NORMAL_TYPE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TYPE),
                TextNode("link", TextType.LINK_TEXT, "https://youtube.com"),
                TextNode(" and another ", TextType.NORMAL_TYPE),
                TextNode(
                    "second link", TextType.LINK_TEXT, "https://google.com"
                ),
            ],
            new_nodes,
        )
        
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        input_text = "This is **bold** and _italic_ and `code` and an ![image](https://example.com) and a [link](https://example.com)."
        expected_output = [
            TextNode("This is ", TextType.NORMAL_TYPE),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.NORMAL_TYPE),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" and ", TextType.NORMAL_TYPE),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.NORMAL_TYPE),
            TextNode("image", TextType.IMG_TEXT, "https://example.com"),
            TextNode(" and a ", TextType.NORMAL_TYPE),
            TextNode("link", TextType.LINK_TEXT, "https://example.com"),
            TextNode(".", TextType.NORMAL_TYPE),
        ]
        
        # Run your function
        actual_output = text_to_textnodes(input_text)
        
        # Assert that the output is correct
       # self.assertEqual(len(actual_output), len(expected_output))

 #       for actual, expected in zip(actual_output, expected_output):
  ###        if hasattr(expected, "meta"):  # Check meta field if it exists
     #           self.assertEqual(actual.meta, expected.meta)


if __name__ == "__main__":
    unittest.main()
