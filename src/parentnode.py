from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All nodes must have a tag")

        if self.children is None:
            raise ValueError("All parent node children must have a value")

        value = ""
        for c in self.children:
            value += c.to_html()

        props = f" {self.props_to_html()}" if len(
            self.props_to_html()) > 0 else ""

        return f"<{self.tag}{props}>{value}</{self.tag}>"
