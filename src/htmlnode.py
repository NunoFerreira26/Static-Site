class HTMLnode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLnode"] | None = None, props: dict[str,str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        #To be implemented by child classes (Leafnode, Parentnode)
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        #Converts internal props dictionary into an HTML attribute string
        if not self.props:
            return ""
        props_html = ""
        for key, val in self.props.items():
            props_html += f' {key}="{val}"'
        return props_html

    def __repr__(self) -> str:
        return f'HTMLnode({self.tag}, {self.value}, children: {len(self.children)}, {self.props})' 

    def __eq__(self, other: object):
        if not isinstance(other, HTMLnode):
            return False
        return ( #True if all their properties are equal
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props 
        )
class ParentNode(HTMLnode): #Parent Class
    def __init__(self, tag: str|None = None, children: list[HTMLnode]|None = None, props: dict[str,str]|None = None):
        super().__init__(tag, value = None, children=children, props=props)
    #tag and children arguments are not optional | It does not take a value argument | props is optional

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if not self.children:
            raise ValueError("All parent nodes have children.")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'

    def __repr__(self) -> str:
        return f"ParentNode({self.tag!r}, children: {len(self.children)}, {self.props})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        )
    
class LeafNode(HTMLnode): #Child class
    def __init__(self, tag: str | None = None, value: str | None = None, props: dict[str,str] | None = None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f'LeafNode({self.tag!r},{self.value!r},{self.props})'
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LeafNode):
            return False
        return ( #True if all their properties are equal
            self.tag == other.tag
            and self.value == other.value
            #and self.children == other.children
            and self.props == other.props 
        )