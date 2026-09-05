import os
import shutil


def copy_static(source: str = "./static", distanation: str = "./docs") -> None:

    if os.path.exists("./docs") and distanation == "./docs":
        shutil.rmtree("./docs")
        os.mkdir("./docs")

    if not os.path.exists(distanation):
        os.mkdir(distanation)

    if os.path.exists(source):
        for filename in os.listdir(source):
            file_path = os.path.join(source, filename)
            dist_path = os.path.join(distanation, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                _ = shutil.copy(file_path, distanation, follow_symlinks=True)
            elif os.path.isdir(file_path):
                copy_static(
                    file_path,
                    dist_path,
                )
