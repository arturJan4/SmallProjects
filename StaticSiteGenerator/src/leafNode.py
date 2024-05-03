from src.HTMLNode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        starting_tag = f"<{self.tag}>"
        tag_attributes = self.props_to_html()
        if len(tag_attributes) > 0:
            starting_tag = f"<{self.tag} {tag_attributes}>"

        closing_tag = f"</{self.tag}>"
        return starting_tag + self.value + closing_tag
