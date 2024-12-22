from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"

        props = f" {self.props_to_html()}" if len(
            self.props_to_html()) > 0 else ""
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
