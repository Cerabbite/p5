import argparse
import importlib.metadata
import os
import pathlib

import requests

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


def download_p5js(path, version="LATEST", addons=False):
    if version == "LATEST":
        version = requests.get("https://registry.npmjs.org/p5/latest").json()["version"]
    else:
        if requests.get(f"https://registry.npmjs.org/p5/{version}").status_code != 200:
            print(
                f"{bcolors.FAIL}Error: Cannot find specified version '{version}' of p5js{bcolors.ENDC}"
            )
            exit(1)

    print(f"{bcolors.OKGREEN}Downloading p5js version {version}{bcolors.ENDC}")
    download = requests.get(
        f"https://github.com/processing/p5.js/releases/download/v{version}/p5.min.js"
    )
    with open(f"{str(path)}\\p5.min.js", "wb") as file_p5:
        file_p5.write(download.content)

    if addons:
        download = requests.get(
            f"https://github.com/processing/p5.js/releases/download/v{version}/p5.min.js"
        )
        with open(f"{str(path)}\\p5.sound.min.js", "wb") as file_p5_sound:
            file_p5_sound.write(download.content)


def create_project(name: str, addons: bool, version):
    path = pathlib.Path(os.getcwd())
    path = path / name
    if os.path.isdir(path):
        print(
            f"{bcolors.FAIL}Error: Directory name '{path}' already exists{bcolors.ENDC}"
        )
        exit(1)

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

    with open(f"{path}\\index.html", "w", encoding="utf-8") as file_index:
        file_index.write(html_template)

    with open(f"{path}\\sketch.js", "w", encoding="utf-8") as file_sketch:
        file_sketch.write(js_template)

    with open(f"{path}\\.gitignore", "w", encoding="utf-8") as file_gitignore:
        file_gitignore.write(gitignore_text)

    download_p5js(path=path, version=version, addons=addons)


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

    args = parser.parse_args()

    if args.command == "create":
        create_project(name=args.name, addons=args.addons, version=args.version)
