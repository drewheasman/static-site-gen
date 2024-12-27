import os, shutil

from generate_page import generate_page


def copy_src_to_dst(src, dst):
    if len(src) == 0 or len(dst) == 0:
        raise Exception("src or dst copy parameters invalid")

    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    print(f"Copying {src} to {dst}")

    if not os.path.exists(src):
        raise Exception("src doesn't exist")

    # Delete dst
    if os.path.isdir(dst):
        print(f"Deleting existing target directory {dst}")
        shutil.rmtree(dst)

    os.mkdir(dst)

    # List dir
    objects = os.listdir(src)
    print("objects", objects)

    # Copy files or recurse for dirs
    for o in objects:
        print(f"Checking {o}")
        if os.path.isfile(f"{src}/{o}"):
            print(f"{o} is file")
            print(f"Copying {src}/{o} to {dst}")
            shutil.copy(f"{src}/{o}", dst)
            continue
        if os.path.isdir(f"{src}/{o}"):
            print(f"{o} is dir")
            copy_src_to_dst(f"{src}/{o}", f"{dst}/{o}")
            continue
    #     else:
    #         raise Exception(f"{o} is not a file or directory?")


def main():
    copy_src_to_dst("./static/", "./public/")
    generate_page("./content/index.md", "template.html", "./public/index.html")


main()
