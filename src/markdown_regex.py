from textnode import *
from htmlnode import *
from text_to_html import *
import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    results= []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TYPE:
            results.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)

        if not links:
            results.append(old_node)
        else:
            current_text = old_node.text
            for link_text, url in links:
                link_markdown =f"[{link_text}]({url})"
                parts = current_text.split(link_markdown, 1)

                if parts[0]:
                    results.append(TextNode(parts[0], TextType.NORMAL_TYPE))

                results.append(TextNode(link_text, TextType.LINK_TEXT, url))
                if len(parts) > 1:
                    current_text = parts[1]
                else:
                    current_text = ""
    return results

def split_nodes_image(old_nodes):
    #a new list to push textType.Text to
    result= []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TYPE:
            result.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        
        if not images:
            # no images found, keep original node
            result.append(old_node)
        else:
            current_text = old_node.text
            for alt_text, url in images:
                image_markdown = f"![{alt_text}]({url})"
                parts = current_text.split(image_markdown, 1)

                if parts[0]:
                    result.append(TextNode(parts[0], TextType.NORMAL_TYPE))
                result.append(TextNode(alt_text, TextType.IMG_TEXT, url))

                if len(parts) > 1:
                    current_text=parts[1]
                else:
                    current_text = ""
    return result

def text_to_textnodes(text):
    segments = split_nodes_delimiter(text)
    text_nodes = []
    i = 0
    while i < len(segments):
        segment = segments[i]
        if segment == "**" and i + 1 < len(segments):
            text_nodes.append(TextNode(segments[i+1], TextType.BOLD_TEXT))
            i += 2
        elif segment == "_" and i + 1 < len(segments):
            text_nodes.append(TextNode(segments[i+1], TextType.ITALIC_TEXT))
            i += 2
        elif segment == "`" and i + 1 < len(segments):
            text_nodes.append(TextNode(segments[i+1], TextType.CODE_TEXT))
            i += 2
        elif segment == "![" and i + 2 < len(segments):
            text_nodes.append(TextNode(segments[i+1], TextType.IMG_TEXT, segments[i+2]))
            i += 3
        elif segment == "[" and i + 2 < len(segments):
            text_nodes.append(TextNode(segments[i+1], TextType.LINK_TEXT, segments[i+2]))
            i += 3
        else:
            text_nodes.append(TextNode(segment, TextType.NORMAL_TYPE))
            i += 1
    return text_nodes