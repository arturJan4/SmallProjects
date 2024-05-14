from src.converterMD import generate_pages_recursive
from src.dirCopy import copy_dirs


def main():
    copy_dirs("markdown_page/static", "public")
    generate_pages_recursive("markdown_page/content/", "markdown_page/template.html", "public/")


if __name__ == "__main__":
    main()
