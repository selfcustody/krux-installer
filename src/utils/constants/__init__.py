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
constants.py

Some constants to be used accros application
"""

from typing import Any
import sys
import os


ROOT_DIRNAME = os.path.abspath(os.path.dirname(__file__))

VALID_DEVICES_VERSIONS = {
    "v25.11.0": [
        "m5stickv",
        "amigo",
        "dock",
        "bit",
        "yahboom",
        "cube",
        "wonder_mv",
        "tzt",
        "embed_fire",
    ],
    "v25.10.1": [
        "m5stickv",
        "amigo",
        "dock",
        "bit",
        "yahboom",
        "cube",
        "wonder_mv",
        "tzt",
    ],
    "v25.10.0": [
        "m5stickv",
        "amigo",
        "dock",
        "bit",
        "yahboom",
        "cube",
        "wonder_mv",
        "tzt",
    ],
    "v25.09.0": ["m5stickv", "amigo", "dock", "bit", "yahboom", "cube", "wonder_mv"],
    "v24.11.0": ["m5stickv", "amigo", "dock", "bit", "yahboom", "cube", "wonder_mv"],
    "v24.09.1": ["m5stickv", "amigo", "dock", "bit", "yahboom", "cube", "wonder_mv"],
    "v24.09.0": ["m5stickv", "amigo", "dock", "bit", "yahboom", "cube", "wonder_mv"],
    "v24.07.0": ["m5stickv", "amigo", "dock", "bit", "yahboom", "cube"],
    "v24.03.0": ["m5stickv", "amigo", "dock", "bit", "yahboom"],
    "v23.09.1": ["m5stickv", "amigo", "dock", "bit"],
    "v23.09.0": ["m5stickv", "amigo", "dock", "bit"],
    "v22.08.2": ["m5stickv", "amigo", "dock", "bit"],
    "v22.08.1": ["m5stickv", "amigo", "dock", "bit"],
    "v22.08.0": ["m5stickv", "amigo", "dock", "bit"],
    "v22.03.0": ["m5stickv"],
    "odudex/krux_binaries": [
        "m5stickv",
        "amigo",
        "dock",
        "bit",
        "yahboom",
        "dock",
        "cube",
        "wonder_mv",
        "tzt",
        "embed_fire",
    ],
}


def _open_pyproject() -> dict[str, Any]:
    """
    Open root pyprojet.toml file to get some constant datas
    like name, version and description
    """
    if sys.version_info.minor <= 10:
        # pylint: disable=import-outside-toplevel,import-error
        from tomli import loads as load_toml
    if sys.version_info.minor > 10:
        # pylint: disable=import-outside-toplevel,import-error
        from tomllib import loads as load_toml

    try:
        pyproject_filename = os.path.abspath(
            os.path.join(ROOT_DIRNAME, "..", "..", "..", "pyproject.toml")
        )
        with open(pyproject_filename, "r", encoding="utf8") as pyproject_file:
            data = pyproject_file.read()
            # pylint: disable=possibly-used-before-assignment
            return load_toml(data)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"{pyproject_filename} isnt found") from exc
    except ValueError as exc:
        raise ValueError(f"{pyproject_filename} is not valid toml file") from exc


def get_name() -> str:
    """
    Get project name defined in pyproject.toml
    """
    return _open_pyproject()["tool"]["poetry"]["name"]


def get_version() -> str:
    """
    Get project version defined in pyproject.toml
    """
    return _open_pyproject()["tool"]["poetry"]["version"]


def get_description() -> str:
    """
    Get project description defined in pyproject.toml
    """
    return _open_pyproject()["tool"]["poetry"]["description"]
