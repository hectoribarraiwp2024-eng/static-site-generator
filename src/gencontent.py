import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    markdown_lines = markdown.split("\n")
    title = ""
    for line in markdown_lines:
        if line.startswith("# "):
            title = line[2:]
    if title == "":
        raise Exception("markdown file must have a title")
    return title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    template = template.replace("{{ Content }}", html)
    template = template.replace("{{ Title }}", title)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    parent_dir = os.path.dirname(dest_path)
    if parent_dir != "":
        os.makedirs(parent_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for path in os.listdir(dir_path_content):

        source_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path)

        if os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, dest_path, basepath)
        elif path.endswith(".md"):
            dest_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(source_path, template_path, dest_path, basepath)
