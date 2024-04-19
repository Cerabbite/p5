import os
import pathlib
import shutil
import unittest
from hashlib import sha256

from p5 import p5

__HASHFILES_PATH__ = pathlib.Path(os.getcwd()) / "test\\hash_files"


class TestP5Cli(unittest.TestCase):
    def test_get_latest_version(self):
        self.assertEqual(p5.get_latest_p5js_version(), "1.9.2")

    def test_download_p5(self):
        if not __HASHFILES_PATH__.is_dir():
            os.mkdir(__HASHFILES_PATH__)

        # v1.6.0
        p5.download_p5js(__HASHFILES_PATH__, version="1.6.0", addons=False)

        with open(__HASHFILES_PATH__ / "p5.min.js", "r", encoding="utf-8") as f:
            contents = f.read()

        self.assertEqual(
            sha256(contents.encode("utf-8")).hexdigest(),
            "9ce766eb93976116171e0ae9875a6facbcd7f498f23b8b9dc61612ea072fc4bd",  # sha256 hash for p5.min.js v1.6.0
        )

        # v1.7.0
        p5.download_p5js(__HASHFILES_PATH__, version="1.7.0", addons=False)

        with open(__HASHFILES_PATH__ / "p5.min.js", "r", encoding="utf-8") as f:
            contents = f.read()

        self.assertEqual(
            sha256(contents.encode("utf-8")).hexdigest(),
            "bb7f8f14b9ce2e2344ff5cd6c06f2e105eb99541ecbfec77139e2886d9c0b9ba",  # sha256 hash for p5.min.js v1.7.0
        )

        # v1.8.0
        p5.download_p5js(__HASHFILES_PATH__, version="1.8.0", addons=False)

        with open(__HASHFILES_PATH__ / "p5.min.js", "r", encoding="utf-8") as f:
            contents = f.read()

        self.assertEqual(
            sha256(contents.encode("utf-8")).hexdigest(),
            "e1ed674bf7491823b1c97e9da899df755c13ae96c0e96630d553ffd1e9867be7",  # sha256 hash for p5.min.js v1.8.0
        )

        # v1.9.0
        p5.download_p5js(__HASHFILES_PATH__, version="1.9.0", addons=False)

        with open(__HASHFILES_PATH__ / "p5.min.js", "r", encoding="utf-8") as f:
            contents = f.read()

        self.assertEqual(
            sha256(contents.encode("utf-8")).hexdigest(),
            "726ac96626b93f5bcaff83a910b6c60d3a9728f063e0eb73b5d0819ffc356915",  # sha256 hash for p5.min.js v1.9.0
        )

        # v1.9.1
        p5.download_p5js(__HASHFILES_PATH__, version="1.9.1", addons=False)

        with open(__HASHFILES_PATH__ / "p5.min.js", "r", encoding="utf-8") as f:
            contents = f.read()

        self.assertEqual(
            sha256(contents.encode("utf-8")).hexdigest(),
            "80d1733dd3f6c84c829a4e9b70fe36649cd5ab1aaef1e2b16d831ae1e54289b2",  # sha256 hash for p5.min.js v1.9.1
        )

        # v1.9.2
        p5.download_p5js(__HASHFILES_PATH__, version="1.9.2", addons=False)

        with open(__HASHFILES_PATH__ / "p5.min.js", "r", encoding="utf-8") as f:
            contents = f.read()

        self.assertEqual(
            sha256(contents.encode("utf-8")).hexdigest(),
            "e2310876d8f60d0b1da36b95c9b3adc3b6f64d1bcc1a609dd13149f70f3f1acc",  # sha256 hash for p5.min.js v1.9.2
        )

        shutil.rmtree(__HASHFILES_PATH__, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
