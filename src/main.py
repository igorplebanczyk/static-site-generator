from textnode import TextNode
from block_markdown import markdown_to_html_node
import os, shutil

def copy_dircontents(src, dest):
    try:
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            else:
                shutil.rmtree(dest)
            files = os.listdir(src)
            for f in files:
                copy_dircontents(os.path.join(src, f), os.path.join(dest, f))
        else:
            shutil.copy(src, dest)
    except Exception as e:
        print(e)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as from_file:
        from_file_contents = from_file.read()

    with open(template_path, "r") as template_file:
        template_file_contents = template_file.read()

    from_file_html = markdown_to_html_node(from_file_contents).to_html()
    title = extract_title(from_file_contents)

    template_file_contents = template_file_contents.replace("{{ Title }}", title)
    template_file_contents = template_file_contents.replace("{{ Content }}", from_file_html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as dest_file:
            dest_file.write(template_file_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path, os.path.splitext(file)[0] + ".html")
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(from_path, template_path, dest_path)


def main():
    textNode = TextNode("Hello World", "text", "https://www.google.com")
    print(repr(textNode))

    copy_dircontents("static/", "public/")
    generate_pages_recursive("content/", "template.html", "public/")

main()