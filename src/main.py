import os
import shutil
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


def copy_site_contents():

    if not os.path.exists(static_path):
        print("static path does not exist")
        os.mkdir(static_path)
    if not os.path.exists(public_path):
        print("public path does not exist")
        os.mkdir(public_path)
    else:
        shutil.rmtree(public_path)

    dir_contents = os.listdir(static_path)

    copy_static_files(dir_contents)


def main():
    text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node)


if __name__ == "__main__":
    main()
