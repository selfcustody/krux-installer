# The MIT License (MIT)

# Copyright (c) 2021-2026 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
.ci/clean.py

Cross-platform cleanup of build artifacts. Removes:
  - build/
  - dist/
  - logs/
  - krux-installer.spec

Usage:
  uv run poe clean
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent.absolute()

TARGETS = [
    ROOT / "build",
    ROOT / "dist",
    ROOT / "logs",
    ROOT / "krux-installer.spec",
]


def clean() -> None:
    for target in TARGETS:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
                print(f"removed dir  {target.relative_to(ROOT)}")
            else:
                target.unlink()
                print(f"removed file {target.relative_to(ROOT)}")
        else:
            print(f"skip (not found) {target.relative_to(ROOT)}")


if __name__ == "__main__":
    clean()