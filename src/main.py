import sys

from copy_content import copy_static
from generate_page import generate_pages_recursive


def main() -> None:
    args = sys.argv
    if len(args) < 2:
        basepath = "/"
    else:
        basepath = args[1]
    copy_static()
    generate_pages_recursive("./content", "template.html", "./docs", basepath)


if __name__ == "__main__":
    main()
