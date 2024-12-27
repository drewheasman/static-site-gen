import os

from block import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node

def generate_pages_recursive(src, template_path, dst):
    if len(src) == 0 or len(dst) == 0:
        raise Exception("src or dst copy parameters invalid")

    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    print(f"Copying {src} to {dst}")

    if not os.path.exists(src):
        raise Exception("src doesn't exist")

    if os.path.isfile(src):
        print(f"{src} is file")
        print(f"Copying {src} to {dst}")
        generate_page(f"{src}", template_path, dst)
        return

    # List dir
    objects = os.listdir(src)
    print("objects", objects)

    # Copy files or recurse for dirs
    for o in objects:
        print(f"Checking {o}")
        if os.path.isfile(f"{src}/{o}"):
            print(f"{o} is file")
            print(f"Copying {src}/{o} to {dst}")
            generate_page(f"{src}/{o}", template_path, dst)
            continue
        if os.path.isdir(f"{src}/{o}"):
            print(f"{o} is dir")
            generate_pages_recursive(f"{src}/{o}", template_path, f"{dst}/{o}")
            continue

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    markdown_from_file = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template_from_file = template_file.read()
    template_file.close()

    title = extract_title(markdown_from_file)
    content = markdown_to_html_node(markdown_from_file).to_html()

    template_from_file = template_from_file.replace("{{ Title }}", title)
    template_from_file = template_from_file.replace("{{ Content }}", content)

    dest_parent_dir = "".join(dest_path.split("/")[:-1])
    if not os.path.exists(dest_parent_dir):
        os.mkdir(dest_parent_dir)

    dest_file = open(dest_path, "w")
    dest_file.write(template_from_file)
    dest_file.close()

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            return block[2:]

    raise Exception("No heading found")
