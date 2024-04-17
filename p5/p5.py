import argparse
import importlib.metadata
import os
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


def create_project(name: str, addons: bool):
    if os.path.isdir(name):
        print(
            f"{bcolors.FAIL}Error: Directory name '{name}' already exists{bcolors.ENDC}"
        )
        exit(1)

    os.mkdir(name)

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

    p5js_text = requests.get(
        "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.2/p5.min.js"
    ).text

    html_file = open(f"{name}\\index.html", "w", encoding="utf-8")
    html_file.write(html_template)
    html_file.close()

    js_file = open(f"{name}\\sketch.js", "w", encoding="utf-8")
    js_file.write(js_template)
    js_file.close()

    p5js_file = open(f"{name}\\p5.min.js", "w", encoding="utf-8")
    p5js_file.write(p5js_text)
    p5js_file.close()

    gitignore_text = "p5.min.js\n"

    if addons:
        p5sound_text = requests.get(
            "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.2/addons/p5.sound.min.js"
        ).text

        p5sound_file = open(f"{name}\\p5.sound.min.js", "w", encoding="utf-8")
        p5sound_file.write(p5sound_text)
        p5sound_file.close()

        gitignore_text += "p5.sound.min.js"

    gitignore_file = open(f"{name}\\.gitignore", "w", encoding="utf-8")
    gitignore_file.write(gitignore_text)
    gitignore_file.close()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    parser_create = subparsers.add_parser("create", help="Create a new p5.js project")
    parser_create.add_argument("name", help="The name of your p5.js project")
    parser_create.add_argument(
        "--addons", action="store_true", help="Include addons to your p5.js project"
    )

    args = parser.parse_args()

    if args.command == "create":
        create_project(args.name, args.addons)
