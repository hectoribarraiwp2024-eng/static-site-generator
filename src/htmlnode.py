class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        html_list = []
        for key in self.props:
            html_list.append(f' {key}="{self.props[key]}\"')
        return "".join(html_list)

    def __repr__(self):
        return f"tag={self.tag}, value={self.value}, children={self.children}, props={self.props}"
        