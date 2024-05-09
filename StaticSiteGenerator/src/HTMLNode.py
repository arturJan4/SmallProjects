from typing import Any, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children=None,
        props=None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, HTMLNode):
            return NotImplemented
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
        # string representation used for debugging
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        # convert node to HTML that's possible to render
        raise NotImplementedError("to_html() not implemented")

    def props_to_html(self) -> str:
        # properties in html are a sequence of key=value assignments
        if not self.props or len(self.props) == 0:
            return ""
        html = []
        for key, value in self.props.items():
            html.append(f'{key}="{value}"')
        return " ".join(html)

    def __get_starting_and_closing_tags__(self) -> tuple[str, str]:
        starting_tag = f"<{self.tag}>"
        tag_attributes = self.props_to_html()
        if len(tag_attributes) > 0:
            starting_tag = f"<{self.tag} {tag_attributes}>"
        closing_tag = f"</{self.tag}>"

        return starting_tag, closing_tag


class LeafNode(HTMLNode):
    # Leaf Node is a node that has no children under it
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")

        if self.tag is None:
            return self.value

        starting_tag, closing_tag = self.__get_starting_and_closing_tags__()

        return starting_tag + self.value + closing_tag


class ParentNode(HTMLNode):
    # Parent Node is a node with other parent nodes or leaves as children
    def __init__(self, children, tag=None, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("Parent nodes must have a children")

        if self.tag is None:
            raise ValueError("Can't produce HTML with no given tag in parent Node")

        starting_tag, closing_tag = self.__get_starting_and_closing_tags__()

        # go through children nodes and recursively generate HTML
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()

        return starting_tag + inner_html + closing_tag
