
class HTMLNode:
    def __init__(self, tag=None, value=None , children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        props_string=""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
        return props_string
        
    def __repr__(self):
        return f"tag:{self.tag} value: {self.value} children:{self.children} props:{self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)

    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError
        if self.tag == None:
            return self.value 
        if self.props is None:
            self.props= {}
        prop_string = ""
        for key, value in self.props.items():
            prop_string += f' {key}= "{value}" '
        prop_string = prop_string.strip()
        if prop_string:
            return f"<{self.tag} {prop_string}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not children or len(children) == 0:
            raise ValueError("a parent node needs at least one child")
        self.children = children
        self.tag = tag
        self.props = props

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError('must have tag')
        if self.children == None or len(self.children) == 0:
            raise ValueError('a parent node needs at least one child')
        for child in self.children:
            if not hasattr(child, "to_html"):
                raise TypeError("All children must be objects that have a to_html method.")
        html_strings = []
        for child in self.children:
            html_strings.append(child.to_html())

        tag_content = ''.join(html_strings)
        return f"<{self.tag}>{tag_content}</{self.tag}>"
        
