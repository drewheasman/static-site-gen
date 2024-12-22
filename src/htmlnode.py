class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        if props is None:
            self.props = {}
        else:
            self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if (self.props is None):
            return ""
        return " ".join(map(lambda p: f'{p[0]}="{p[1]}"', self.props.items()))

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        ):
            return True
        return False
