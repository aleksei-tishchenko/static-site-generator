import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splited: list[TextNode] = []
        nodes_text = node.text.split(delimiter)
        if len(nodes_text) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(nodes_text)):
            if nodes_text[i] == "":
                continue
            if i % 2 == 0:
                splited.append(TextNode(nodes_text[i], TextType.TEXT))
            else:
                splited.append(TextNode(nodes_text[i], text_type))
        new_nodes.extend(splited)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        original_text = node.text
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            splited = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(splited) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if splited[0] != "":
                new_nodes.append(TextNode(splited[0], TextType.TEXT))
            image_node = TextNode(image_alt, TextType.IMAGE, image_link)
            original_text = splited[1]
            new_nodes.append(image_node)
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        original_text = node.text
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            link_alt = link[0]
            link_url = link[1]
            splited = original_text.split(f"[{link_alt}]({link_url})", 1)
            if len(splited) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if splited[0] != "":
                new_nodes.append(TextNode(splited[0], TextType.TEXT))
            image_node = TextNode(link_alt, TextType.LINK, link_url)
            original_text = splited[1]
            new_nodes.append(image_node)
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
