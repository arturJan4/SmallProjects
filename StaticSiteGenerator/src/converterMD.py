import os
import pathlib

from src.markdownNodeGen import markdown_to_html


def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line
    raise ValueError("No h1 header found, when it's required")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from file: {from_path} to: {dest_path}, using template {template_path}")

    if not os.path.exists(from_path):
        raise FileExistsError(f"{from_path} doesn't exists")

    if not os.path.exists(template_path):
        raise FileExistsError(f"{template_path} doesn't exists")

    markdown = ""
    with open(from_path, "r") as file:
        markdown = file.read()

    template = ""
    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    # create required directories
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise FileExistsError(f"{dir_path_content} doesn't exists")

    if not os.path.exists(template_path):
        raise FileExistsError(f"{template_path} doesn't exists")

    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)

        if os.path.isfile(file_path):
            output_filename = pathlib.Path(file_path).with_suffix(".html").name
            print(output_filename)
            output_path = os.path.join(dest_dir_path, output_filename)
            print(output_path)
            generate_page(file_path, template_path, output_path)

        if os.path.isdir(file_path):
            output_dir = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(file_path, template_path, output_dir)
