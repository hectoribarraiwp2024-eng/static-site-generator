from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_old_nodes = old_node.text.split(delimiter)
        if len(split_old_nodes) % 2 != 1:
            raise Exception("invalid markdown syntax")
        for i in range(len(split_old_nodes)):
            if split_old_nodes[i] == "":
                continue
            if i % 2 == 1:
                node = TextNode(split_old_nodes[i], text_type)
                new_nodes.append(node)
            else:
                node = TextNode(split_old_nodes[i], TextType.TEXT)
                new_nodes.append(node)
    return new_nodes