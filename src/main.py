from copy_content import copy_static
from generate_page import generate_pages_recursive


def main() -> None:
    copy_static()
    generate_pages_recursive("./content", "template.html", "./public")


if __name__ == "__main__":
    main()
