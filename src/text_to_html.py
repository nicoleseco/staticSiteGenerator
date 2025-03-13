from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TYPE:
        #return leafnode with no tag, just text
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        #return a leafnode with 'b' tag
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        #return 'i' tag
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        #return 'code' tag
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TextType.LINK_TEXT:
        #return 'a' tag, anchor text, and href prop
        return LeafNode('code', text_node.text, {'href': text_node.url})
    elif text_node.text_type == TextType.IMG_TEXT:
        #return 'img' tag, empty string value, 'src' and 'alt' props ('src' is image url, 'alt' is alt text)
        return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})
    else:
        raise Exception(f"Infalid TextType: {text_node.text_type}")
    


def split_nodes_delimiter(text):
    result = []
    delimiters = ["**", "_", "`", "![", "["]
    i = 0
    
    while text:
        matched = False
        for delimiter in delimiters:
            if text[i:i+len(delimiter)] == delimiter:
                if i > 0:
                    result.append(text[0:i])
                result.append(delimiter)
                text = text[i+len(delimiter):]
                matched = True
                break
        if not matched:
            next_delim_index = len(text)
            for delimiter in delimiters:
                index = text.find(delimiter)
                if index != -1 and index < next_delim_index:
                    next_delim_index = index
            result.append(text[:next_delim_index])
            text = text[next_delim_index:]
    return result