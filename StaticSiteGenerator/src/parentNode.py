from src.HTMLNode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("Parent nodes must have a children.")
        
        if self.tag is None:
            raise ValueError("Can't produce HTML with no given tag in parent Node.")

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
