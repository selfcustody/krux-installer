# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

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
build.py
"""
from pathlib import Path
from platform import system
import PyInstaller.__main__

# build executable for following systems
if system() not in ("Linux", "Windows", "Darwin"):
    raise OSError(f"OS '{system()}' not implemented")

# Get root path to properly setup
ROOT_PATH = Path(__file__).parent.parent.absolute()
PYNAME = "krux-installer"
PYFILE = f"{PYNAME}.py"
KFILE = str(ROOT_PATH / PYFILE)
BUILDER_ARGS = [
    PYFILE,
    "--add-data=pyproject.toml:.",
    "--add-data=krux_installer.kv:.",
    "--windowed",
    "--onefile",
    f"-n={PYNAME}",
]
print("RUN " + " \\\n ".join(BUILDER_ARGS))
print()

# Now build
PyInstaller.__main__.run(BUILDER_ARGS)
