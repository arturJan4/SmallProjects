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
        raise NotImplementedError

    def props_to_html(self):
        if not self.props or len(self.props) == 0:
            return ""
        html = []
        for key, value in self.props.items():
            html.append(f'{key}="{value}"')
        return " ".join(html)
