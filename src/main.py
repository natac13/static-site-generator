import os
import shutil
from block_markdown import markdown_to_html_node
from textnode import TextNode

static_path = os.path.join(".", "static")
public_path = os.path.join(".", "public")


def copy_static_files(dir_contents, parent_path=""):
    for item in dir_contents:
        item_path = os.path.join(static_path, parent_path, item)
        public_item_path = os.path.join(public_path, parent_path, item)
        print(item_path)
        print(public_item_path)

        if not os.path.isfile(item_path):
            if not os.path.exists(public_item_path):
                os.mkdir(public_item_path)
            sub_dir_contents = os.listdir(item_path)
            copy_static_files(sub_dir_contents, os.path.join(parent_path, item))
        else:
            shutil.copy(item_path, public_item_path)


def extract_title(markdown):
    """
    Grab the text of the h1 header from the markdown file (The line that starts with a single #) and return it. If there is no h1 header, raise an exception. All pages need a single h1 header.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read the incoming markdown file
    with open(from_path, "r") as f:
        markdown = f.read()
    # read the template file
    with open(template_path, "r") as f:
        template = f.read()
    # convert the markdown to html
    html = markdown_to_html_node(markdown).to_html()
    # extract the title from the markdown
    title = extract_title(markdown)
    # replace the title and content in the template
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    # write the generated page to the destination
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_contents = os.listdir(dir_path_content)
    for item in dir_path_contents:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            generate_pages_recursive(
                item_path, template_path, os.path.join(dest_dir_path, item)
            )
        elif item.endswith(".md"):
            generate_page(
                item_path,
                template_path,
                os.path.join(dest_dir_path, item[:-3] + ".html"),
            )


def copy_site_contents():

    if not os.path.exists(static_path):
        print("static path does not exist")
        os.mkdir(static_path)
    if not os.path.exists(public_path):
        print("public path does not exist")
        os.mkdir(public_path)
    else:
        shutil.rmtree(public_path)
        os.mkdir(public_path)

    dir_contents = os.listdir(static_path)

    copy_static_files(dir_contents)


# Also, update your main.sh script to start a simple web server after generating the site. Python has a built-in file server.
def main():
    copy_site_contents()

    generate_pages_recursive(
        os.path.join(".", "content"),
        os.path.join(".", "template.html"),
        os.path.join(public_path),
    )

    # Start a simple web server
    # os.system(f"python -m http.server --directory {public_path}")


if __name__ == "__main__":
    main()
