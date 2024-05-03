class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, value: object) -> bool:
        if self.tag != value.tag:
            return False
        if self.value != value.value:
            return False
        if self.children != value.children:
            return False
        if self.props != value.props:
            return False
        return True

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html() not implemented")

    def props_to_html(self):
        if not self.props or len(self.props) == 0:
            return ""
        html = []
        for key, value in self.props.items():
            html.append(f'{key}="{value}"')
        return " ".join(html)


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")

        if self.tag is None:
            return self.value

        starting_tag = f"<{self.tag}>"
        tag_attributes = self.props_to_html()
        if len(tag_attributes) > 0:
            starting_tag = f"<{self.tag} {tag_attributes}>"

        closing_tag = f"</{self.tag}>"
        return starting_tag + self.value + closing_tag


class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("Parent nodes must have a children")

        if self.tag is None:
            raise ValueError("Can't produce HTML with no given tag in parent Node")

        starting_tag = f"<{self.tag}>"
        tag_attributes = self.props_to_html()
        if len(tag_attributes) > 0:
            starting_tag = f"<{self.tag} {tag_attributes}>"
        closing_tag = f"</{self.tag}>"

        # go through children nodes and recursively generate HTML
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()

        return starting_tag + inner_html + closing_tag
