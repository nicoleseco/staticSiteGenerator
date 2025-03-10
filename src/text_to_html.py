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
        raise Exception(f"Infalid TextType: {tex_node.text_type}")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #print parameters for debugging
    print(old_nodes)
    print(delimiter)
    print(text_type)
    #a new list to push TextType.TEXT to 
    new_list = []
    #iterate through old_nodes, if not TextType.TEXT, push to new list
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TYPE:
            new_list.append(old_node)
        else:
            segments = old_node.text.split(delimiter)
            if len(segments) % 2 == 0:
                raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {old_node.text}")

            is_inside_delimiter = False
            for segment in segments:
                if is_inside_delimiter:
                    new_node = TextNode(segment, text_type)
                else:
                    new_node = TextNode(segment, TextType.NORMAL_TYPE)
                new_list.append(new_node)
                is_inside_delimiter = not is_inside_delimiter
    return new_list