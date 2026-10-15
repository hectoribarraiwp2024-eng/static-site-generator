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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    template = template.replace("{{ Content }}", html)
    template = template.replace("{{ Title }}", title)

    if parent_dir != "":
        parent_dir = os.path.dirname(dest_path)

    os.makedirs(parent_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)