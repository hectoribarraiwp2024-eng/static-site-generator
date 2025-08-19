from textnode import TextType, TextNode, BlockType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    text = old_nodes.text
    image_pair = extract_markdown_images(text)
    for i in range(len(image_pair)):
        alt, link = image_pair[i][0], image_pair[i][1]
        if i == 0:
            text_list = text.split(f"![{alt}]({link})")
        else:
            temp = text_list.pop()
            text_list.extend(temp.split(f"![{alt}]({link})"))
    for i in range(len(image_pair)):
        new_nodes.append(TextNode(text_list[i], TextType.TEXT))
        new_nodes.append(TextNode(image_pair[i][0], TextType.IMAGE, image_pair[i][1]))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    text = old_nodes.text
    image_pair = extract_markdown_links(text)
    for i in range(len(image_pair)):
        alt, link = image_pair[i][0], image_pair[i][1]
        if i == 0:
            text_list = text.split(f"[{alt}]({link})")
        else:
            temp = text_list.pop()
            text_list.extend(temp.split(f"[{alt}]({link})"))
    for i in range(len(image_pair)):
        new_nodes.append(TextNode(text_list[i], TextType.TEXT))
        new_nodes.append(TextNode(image_pair[i][0], TextType.LINK, image_pair[i][1]))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    end_node = new_nodes[2]
    end_nodes = split_nodes_delimiter([end_node], "_", TextType.ITALIC)
    new_nodes.pop()
    new_nodes.extend(end_nodes)
    end_node = new_nodes[4]
    end_nodes = split_nodes_delimiter([end_node], "`", TextType.CODE)
    new_nodes.pop()
    new_nodes.extend(end_nodes)
    end_node = new_nodes[6]
    end_nodes1 = split_nodes_image(end_node)
    end_nodes2 = split_nodes_link(end_node)
    new_nodes.pop()
    new_nodes.extend(end_nodes1)
    new_nodes.append(TextNode(" and a ", TextType.TEXT))
    new_nodes.append(end_nodes2[1])
    print()
    print()
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks]
    return blocks


def block_to_block_type(block):
    if '#' in block[:7]:
        return BlockType.HEADING
    if block[:3] == '```' and block[-3:] == '```':
        return BlockType.CODE
    if '>' == block[0]:
        return BlockType.QUOTE
    if '-' == block[0]:
        return BlockType.UNORDERED_LIST
    if '.' == block[1]:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

