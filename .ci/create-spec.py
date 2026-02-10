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
import argparse
import PyInstaller.building.makespec

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    PyInstaller.building.makespec.__add_options(p)
    PyInstaller.log.__add_options(p)

    SYSTEM = system()

    # build executable for following systems
    if SYSTEM not in ("Linux", "Windows", "Darwin"):
        raise OSError(f"OS '{system()}' not implemented")

    # Get root path to properly setup
    DIR = Path(__file__).parents
    ROOT_PATH = Path(__file__).parent.parent.absolute()
    PYNAME = "krux-installer"
    PYFILE = f"{PYNAME}.py"
    KFILE = str(ROOT_PATH / PYFILE)
    ASSETS = str(ROOT_PATH / "assets")
    ICON = join(ASSETS, "icon.png")
    I18NS = str(ROOT_PATH / "src" / "i18n")

    if SYSTEM == "Darwin":
        ICON = join(ASSETS, "icon.icns")
    elif SYSTEM == "Windows":
        ICON = join(ASSETS, "icon.ico")
    else:
        ICON = join(ASSETS, "icon.png")

    BUILDER_ARGS = []

    # The app name
    BUILDER_ARGS.append(f"--name={PYNAME}")

    # The application has window
    BUILDER_ARGS.append("--windowed")

    # Icon
    BUILDER_ARGS.append(f"--icon={ICON}")

    # Specifics about operational system
    # on how will behave as file or bundled app
    if SYSTEM == "Linux":
        # Tha application is a GUI
        BUILDER_ARGS.append("--onefile")

    elif SYSTEM == "Windows":
        # Tha application is a GUI with a hidden console
        # to keep `sys` module enabled (necessary for Kboot)
        BUILDER_ARGS.append("--onefile")
        BUILDER_ARGS.append("--console")
        BUILDER_ARGS.append("--hidden-import=win32timezone")
        BUILDER_ARGS.append("--hide-console=minimize-early")

    elif SYSTEM == "Darwin":
        # Tha application is a GUI in a bundled .app
        BUILDER_ARGS.append("--onefile")
        BUILDER_ARGS.append("--noconsole")

        # For darwin system, will be necessary
        # to add a hidden import for ssl
        # (necessary for request module)
        BUILDER_ARGS.append("--hidden-import=ssl")
        BUILDER_ARGS.append("--optimize=2")

    # Necessary for get version and
    # another infos in application
    BUILDER_ARGS.append("--add-data=pyproject.toml:.")

    # some assets
    for f in listdir(ASSETS):
        asset = join(ASSETS, f)
        if isfile(asset):
            if asset.endswith("png") or asset.endswith("gif") or asset.endswith("ttf"):
                BUILDER_ARGS.append(f"--add-data={asset}:assets")

    # Add i18n translations
    for f in listdir(I18NS):
        i18n_abs = join(I18NS, f)
        i18n_rel = join("src", "i18n")
        if isfile(i18n_abs):
            if findall(r"^[a-z]+\_[A-Z]+\.UTF-8\.json$", f):
                BUILDER_ARGS.append(f"--add-data={i18n_abs}:{i18n_rel}")

    args = p.parse_args(BUILDER_ARGS)

    # Now generate spec
    print("============================")
    print("create-spec.py")
    print("============================")
    print()
    for k, v in vars(args).items():
        print(f"{k}: {v}")

    print()
    PyInstaller.building.makespec.main(["krux_installer.py"], **vars(args))
