from textnode import TextNode, TextType


def main():
    my_node = TextNode(
        "This is a text node",
        TextType.BOLD,
        "https://www.boot.dev")
    print(my_node)


main()
