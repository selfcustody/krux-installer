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
from re import findall
from os import listdir
from os.path import join, isfile
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
I18NS = str(ROOT_PATH / "src" / "i18n")

BUILDER_ARGS = [
    PYFILE,
    "--add-data=pyproject.toml:.",
    "--add-data=krux_installer.kv:.",
]

# Add i18n translations

for f in listdir(I18NS):
    i18n_abs = join(I18NS, f)
    i18n_rel = join("src", "i18n")
    if isfile(i18n_abs):
        if findall(r"^[a-z]+\_[A-Z]+\.UTF-8\.json$", f):
            BUILDER_ARGS.append(f"--add-data={i18n_abs}:{i18n_rel}")


BUILDER_ARGS.append("--windowed")
BUILDER_ARGS.append("--onefile")
BUILDER_ARGS.append(f"-n={PYNAME}")

print("RUN " + " \\\n ".join(BUILDER_ARGS))
print()

# Now build
PyInstaller.__main__.run(BUILDER_ARGS)
