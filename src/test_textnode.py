import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK_TEXT)
        node2 = TextNode("This is a link", TextType.LINK_TEXT)
        self.assertEqual(node, node2)

    def test_img(self):
        node = TextNode("picture!", TextType.IMG_TEXT)
        node2 = TextNode("pretty", TextType.IMG_TEXT)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
