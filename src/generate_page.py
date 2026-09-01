import os
from pathlib import Path

from markdown_blocks import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_file: str = f.read()
    with open(template_path, "r") as f:
        template_file = f.read()
    html_string = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    content = template_file.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for entity in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entity)
        dest_path = os.path.join(dest_dir_path, "index.html")
        if os.path.isfile(full_path):
            with open(full_path, "r") as f:
                markdown_file: str = f.read()
            with open(template_path, "r") as f:
                template_file = f.read()
            html_string = markdown_to_html_node(markdown_file).to_html()
            title = extract_title(markdown_file)
            content = template_file.replace("{{ Title }}", title).replace(
                "{{ Content }}", html_string
            )
            full_dest_path = os.path.dirname(dest_path)
            if full_dest_path != "":
                os.makedirs(full_dest_path, exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            generate_pages_recursive(
                full_path, template_path, os.path.join(dest_dir_path, entity)
            )
