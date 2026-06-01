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
create-spec.py

Generates the PyInstaller .spec file for krux-installer.

Terminal output is controlled by the BUILD_LOGLEVEL environment variable,
set automatically by the poe build tasks via the --debug flag:

    poetry run poe build-macos              # silent (default: WARN)
    poetry run poe build-macos --debug=INFO # prints spec args summary
    poetry run poe build-macos --debug=DEBUG  # prints spec args summary
    poetry run poe build-macos --debug=TRACE  # prints spec args summary

Allowed values: TRACE | DEBUG | INFO | WARN | ERROR | CRITICAL
"""

import argparse
import os
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path
from platform import system
from re import findall

import PyInstaller.building.makespec

from src.utils.constants import FIRMWARE_VERSION

_VALID_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"}
_VERBOSE_LEVELS = {"TRACE", "DEBUG", "INFO"}


def _parse_loglevel() -> str:
    """Read --loglevel from CLI args, fallback to BUILD_LOGLEVEL env var."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--loglevel",
        default=os.environ.get("BUILD_LOGLEVEL", "WARN"),
        choices=list(_VALID_LEVELS),
        type=str.upper,
    )
    args, _ = parser.parse_known_args()
    return args.loglevel


_LOGLEVEL = _parse_loglevel()


def _is_verbose() -> bool:
    """Return True if loglevel is INFO or below."""
    return _LOGLEVEL in _VERBOSE_LEVELS


def _log(msg: str = "") -> None:
    """Print only when running in verbose mode."""
    if _is_verbose():
        print(msg)


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
        # The application is a GUI
        BUILDER_ARGS.append("--onefile")

    elif SYSTEM == "Windows":
        # The application is a GUI with a hidden console
        # to keep `sys` module enabled (necessary for Kboot)
        BUILDER_ARGS.append("--onefile")
        BUILDER_ARGS.append("--console")
        BUILDER_ARGS.append("--hidden-import=win32timezone")
        BUILDER_ARGS.append("--hide-console=minimize-early")

    elif SYSTEM == "Darwin":
        # The application is a GUI in a bundled .app
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

    # Add embedded firmware binaries
    FIRMWARE_PATH = str(ROOT_PATH / "src" / "utils" / "firmware" / FIRMWARE_VERSION)
    FIRMWARE_DEST = join("src", "utils", "firmware", FIRMWARE_VERSION)
    for f in listdir(FIRMWARE_PATH):
        fw_abs = join(FIRMWARE_PATH, f)
        if isfile(fw_abs) and f.endswith(".kfpkg"):
            BUILDER_ARGS.append(f"--add-data={fw_abs}:{FIRMWARE_DEST}")

    args = p.parse_args(BUILDER_ARGS)

    # Print spec summary only when running in verbose mode
    _log("============================")
    _log("create-spec.py")
    _log("============================")
    _log()
    for k, v in vars(args).items():
        _log(f"{k}: {v}")
    _log()

    import os as _os

    if _is_verbose():
        PyInstaller.building.makespec.main(["krux_installer.py"], **vars(args))
    else:
        # PyInstaller writes DEPRECATION warnings directly to the stderr file
        # descriptor — contextlib.redirect_stderr is not enough. We redirect
        # fd 2 to /dev/null at the OS level for the duration of this call.
        devnull_fd = _os.open(_os.devnull, _os.O_WRONLY)
        old_stderr_fd = _os.dup(2)
        try:
            _os.dup2(devnull_fd, 2)
            PyInstaller.building.makespec.main(["krux_installer.py"], **vars(args))
        finally:
            _os.dup2(old_stderr_fd, 2)
            _os.close(old_stderr_fd)
            _os.close(devnull_fd)