import argparse
import importlib.metadata
import os
import pathlib
import re
import shutil

import requests
import tomllib
from packaging.version import Version

__METADATA__ = importlib.metadata.metadata("p5")
__NAME__ = __METADATA__["NAME"]
__DESCRIPTION__ = __METADATA__["SUMMARY"]
__VERSION__ = __METADATA__["VERSION"]
__LICENSE__ = __METADATA__["LICENSE"]


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Error:
    def __init__(self, msg):
        print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")


class InvalidVersionNumberError(Error):
    def __init__(self, msg):
        new_msg = f"InvalidVersionNumber error: {msg}"
        super().__init__(new_msg)


def read_p5_toml(path):
    with open(path / "p5.toml", "rb") as f:
        data = tomllib.load(f)
        version = data["p5js"]["version"]
        addons = data["p5js"]["addons"]

    return (version, addons)


def get_latest_p5js_version():
    return requests.get("https://registry.npmjs.org/p5/latest").json()["version"]


def download_p5js(path, version="LATEST", addons=False) -> Error | None:
    if version == "LATEST":
        version = get_latest_p5js_version()
    else:
        if requests.get(f"https://registry.npmjs.org/p5/{version}").status_code != 200:
            # raise InvalidVersionNumber(
            #     f"Error: Cannot find specified version '{version}' of p5js"
            # )
            return InvalidVersionNumberError(f"Cannot find `{version}` of p5js")

    print(f"Downloading p5js version {version}")
    download = requests.get(
        f"https://github.com/processing/p5.js/releases/download/v{version}/p5.min.js"
    )
    if download.status_code != 200:
        print(f"{bcolors.FAIL}Cannot download version '{version}' of p5js{bcolors.ENDC}")
        exit(1)

    with open(f"{str(path)}\\p5.min.js", "wb") as file_p5:
        file_p5.write(download.content)

    if addons:
        download = requests.get(
            f"https://github.com/processing/p5.js/releases/download/v{version}/p5.min.js"
        )
        if download.status_code != 200:
            print(
                f"{bcolors.FAIL}Error: Cannot download version '{version}' of p5js{bcolors.ENDC}"
            )
            exit(1)
        with open(f"{str(path)}\\p5.sound.min.js", "wb") as file_p5_sound:
            file_p5_sound.write(download.content)


def create_project(name, addons, version):
    path = pathlib.Path(os.getcwd())
    path = path / name
    existing_path = os.path.isdir(path)
    if existing_path:
        print(
            f"{bcolors.WARNING}Warning: Directory name '{path}' already exists{bcolors.ENDC}"
        )
        while True:
            q = input("Do you wish to continue? (y/n) ")
            if q.lower() == "y":
                break
            elif q.lower() == "n":
                print("Exiting program")
                return
    else:
        os.mkdir(path)

    gitignore_text = "p5.min.js\n"

    html_template = """<!DOCTYPE html>
<html lang="">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>p5.js example</title>
  <style>
    body {
      padding: 0;
      margin: 0;
      background-color: #1b1b1b;
    }
  </style>
  <script src="p5.min.js"></script>
  <script src="sketch.js"></script>"""
    if addons:
        html_template += """\n  <script src="../addons/p5.sound.js"></script>"""
        gitignore_text += "p5.sound.min.js"

    html_template += """\n</head>

<body>
  <main>
  </main>
</body>

</html>"""

    js_template = """function setup() {
  createCanvas(320, 240);
}


function draw() {
  background(0);
  ellipse(100, 120, 16, 16);
}"""

    if version == "LATEST":
        version = get_latest_p5js_version()

    p5_toml = f"""[p5js]
version = "{version}"
addons = {str(addons).lower()}"""

    with open(f"{path}\\index.html", "w", encoding="utf-8") as file_index:
        file_index.write(html_template)

    with open(f"{path}\\sketch.js", "w", encoding="utf-8") as file_sketch:
        file_sketch.write(js_template)

    with open(f"{path}\\.gitignore", "w", encoding="utf-8") as file_gitignore:
        file_gitignore.write(gitignore_text)

    with open(f"{path}\\p5.toml", "w", encoding="utf-8") as file_p5_toml:
        file_p5_toml.write(p5_toml)

    ret_val = download_p5js(path=path, version=version, addons=addons)
    if isinstance(ret_val, Error):
        if not existing_path:
            shutil.rmtree(path)
        return ret_val

    print(
        f"{bcolors.OKGREEN}Successfully created p5js project {name} v{version}{bcolors.ENDC}"
    )


def upgrade_project(name, version) -> Error | None:
    path = pathlib.Path(os.getcwd())
    if name:
        path = path / name

    path_p5 = path / "p5.min.js"
    path_p5_sound = path / "p5.sound.min.js"

    extract_version = r"v(\d+\.\d+\.\d+)"

    latest = False
    addons = False

    if path_p5.is_file():
        with open(path_p5, "r", encoding="utf-8") as f:
            current_version_p5 = re.search(extract_version, str(f.readlines()[0]))
            if not current_version_p5:
                current_version_p5 = "1.0.0"
                print(
                    f"{bcolors.FAIL}Warning: Cannot read p5.min.js version setting version number to {current_version_p5}{bcolors.ENDC}"
                )
            else:
                current_version_p5 = current_version_p5.group(1)
        print(f"Found p5.min.js version {current_version_p5}")
    else:
        print(f"{bcolors.FAIL}Error: Cannot find p5.min.js{bcolors.ENDC}")
        exit(1)

    if path_p5_sound.is_file():
        with open(path_p5_sound, "r", encoding="utf-8") as f:
            current_version_p5_sound = re.search(extract_version, str(f.readlines()[0]))
            if not current_version_p5_sound:
                current_version_p5_sound = "1.0.0"
                print(
                    f"{bcolors.FAIL}Warning: Cannot read p5.min.js version setting version number to {current_version_p5_sound}{bcolors.ENDC}"
                )
            else:
                current_version_p5_sound = current_version_p5_sound.group(1)
        print(f"Found p5.sound.min.js version {current_version_p5_sound}")

        addons = True

    if version == "LATEST":
        version = get_latest_p5js_version()
        latest = True

    if Version(current_version_p5) == Version(version):
        if latest:
            print(
                f"{bcolors.WARNING}Warning: You are already on the latest version of p5js.{bcolors.ENDC}"
            )
        else:
            print(
                f"{bcolors.WARNING}Warning: You are already on your desired version of p5js.{bcolors.ENDC}"
            )
        exit(0)

    if Version(current_version_p5) >= Version(version):
        while True:
            downgrade = input(
                f"{bcolors.WARNING}Warning: You are currently on version {current_version_p5} of p5js do you want to downgrade to version {version}? (y/n) {bcolors.ENDC}"
            ).lower()
            if downgrade == "y":
                print(f"Downgrading to {version}")
                break
            elif downgrade == "n":
                exit(0)

    ret_val = download_p5js(path=path, version=version, addons=addons)
    if isinstance(ret_val, Error):
        return ret_val


def clear_project(name):
    path = pathlib.Path(os.getcwd())
    if name:
        path = path / name

    if not (path / "p5.toml").is_file():
        print(f"{bcolors.FAIL}Error: could not find `p5.toml` file{bcolors.ENDC}")
        exit(1)

    addons = read_p5_toml(path)[1]

    if (path / "p5.min.js").is_file():
        os.remove(path / "p5.min.js")
    else:
        print(f"{bcolors.WARNING}Warning: could not find p5.min.js{bcolors.ENDC}")

    if addons:
        if (path / "p5.sound.min.js").is_file():
            os.remove(path / "p5.sound.min.js")
        else:
            print(
                f"{bcolors.WARNING}Warning: could not find p5.sound.min.js{bcolors.ENDC}"
            )

    print(f"{bcolors.OKGREEN}Successfully cleared `{name}` {bcolors.ENDC}")


def reinstate_project(name) -> Error | None:
    path = pathlib.Path(os.getcwd())
    if name:
        path = path / name

    version, addons = read_p5_toml(path)

    ret_val = download_p5js(path=path, version=version, addons=addons)
    if isinstance(ret_val, Error):
        return ret_val

    print(f"{bcolors.OKGREEN}Successfully reinstated `{name}` {bcolors.ENDC}")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    create_arg = subparsers.add_parser("create", help="Create a new p5.js project")
    create_arg.add_argument("name", help="The name of your p5.js project")
    create_arg.add_argument(
        "--addons", action="store_true", help="Include addons to your p5.js project"
    )
    create_arg.add_argument(
        "--version", help="Specify version of p5.js to download", default="LATEST"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__VERSION__),
    )

    upgrade_arg = subparsers.add_parser("upgrade", help="Upgrade p5.js")
    upgrade_arg.add_argument(
        "name",
        help="[OPTIONAL] Specify the name of the p5.js project to upgrade",
        nargs="?",
    )
    upgrade_arg.add_argument(
        "--version", help="Specify version of p5.js to download", default="LATEST"
    )

    clear_arg = subparsers.add_parser("clear", help="Clear a p5.min.js files")
    clear_arg.add_argument(
        "name",
        help="[OPTIONAL] Specify the name of the p5.js project to upgrade",
        nargs="?",
    )

    reinstate_arg = subparsers.add_parser("reinstate", help="Reinstate a p5js project")
    reinstate_arg.add_argument(
        "name",
        help="[OPTIONAL] Specify the name of the p5.js project to upgrade",
        nargs="?",
    )

    args = parser.parse_args()

    ret_val = None

    if args.command == "create":
        ret_val = create_project(name=args.name, addons=args.addons, version=args.version)
    elif args.command == "upgrade":
        ret_val = upgrade_project(args.name, args.version)
    elif args.command == "clear":
        ret_val = clear_project(args.name)
    elif args.command == "reinstate":
        ret_val = reinstate_project(args.name)

    if ret_val:
        print(f"{bcolors.FAIL}p5 exited with an error{bcolors.ENDC}")
        exit(1)
