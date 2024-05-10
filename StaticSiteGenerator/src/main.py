from dirCopy import copy_dirs
from textNode import TextNode


def main():
    example = TextNode("example test node", "italic", "example.com")
    print(example)

    copy_dirs("static", "public")


if __name__ == "__main__":
    main()
