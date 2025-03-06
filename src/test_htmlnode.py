import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})

    def test_tag_empty(self):
        node = HTMLNode(tag="")
    def test_value_empty(self):
        node = HTMLNode(value="")
    def test_children_empty(self):
        node = HTMLNode(children=[])

if __name__ == "__main__":
    unittest.main()
