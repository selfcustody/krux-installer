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

from typing import Any, List
import sys
import os
import re


ROOT_DIRNAME = os.path.abspath(os.path.dirname(__file__))

VALID_DEVICES = [
    "m5stickv",
    "amigo",
    "dock",
    "bit",
    "yahboom",
    "cube",
    "wonder_mv",
    "tzt",
    "embed_fire",
]

VALID_DEVICES_VERSIONS = {
    "m5stickv": {
        "initial": "v22.03.0",
        "final": None,
    },
    "amigo": {
        "initial": "v22.08.0",
        "final": None,
    },
    "dock": {
        "initial": "v22.08.0",
        "final": None,
    },
    "bit": {
        "initial": "v22.08.0",
        "final": "v25.10.0",
    },
    "yahboom": {
        "initial": "v24.03.0",
        "final": None,
    },
    "cube": {
        "initial": "v24.07.0",
        "final": None,
    },
    "wonder_mv": {
        "initial": "v24.09.0",
        "final": None,
    },
    "tzt": {
        "initial": "v25.10.0",
        "final": None,
    },
    "embed_fire": {
        "initial": "v25.11.0",
        "final": None,
    },
}


def _parse_version(version: str) -> tuple:
    """
    Parse version string into comparable tuple.

    Args:
        version: Version string in format 'vYY.MM.P' (e.g., 'v22.03.0')

    Returns:
        Tuple of integers (year, month, patch) for comparison
        Returns (0, 0, 0) if parsing fails
    """
    match = re.match(r"^v(\d+)\.(\d+)\.(\d+)$", version)
    if match:
        return tuple(map(int, match.groups()))
    return (0, 0, 0)


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version strings.

    Args:
        version1: First version string
        version2: Second version string

    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    """
    v1_tuple = _parse_version(version1)
    v2_tuple = _parse_version(version2)

    if v1_tuple < v2_tuple:
        return -1
    if v1_tuple > v2_tuple:
        return 1
    return 0


def is_device_valid_for_version(device: str, version: str) -> bool:
    """
    Check if a device is valid for a specific Krux version.

    Args:
        device: Device name (e.g., 'm5stickv', 'amigo', etc.)
        version: Version string (e.g., 'v24.03.0')

    Returns:
        True if device is compatible with the version, False otherwise
    """
    if device not in VALID_DEVICES_VERSIONS:
        return False

    device_info = VALID_DEVICES_VERSIONS[device]
    initial_version = device_info["initial"]
    final_version = device_info["final"]

    if compare_versions(version, initial_version) < 0:
        return False

    if final_version is not None and compare_versions(version, final_version) > 0:
        return False

    return True


def get_valid_devices_for_version(version: str) -> List[str]:
    """
    Get list of valid devices for a specific Krux version.

    Args:
        version: Version string (e.g., 'v24.03.0')

    Returns:
        List of device names that are compatible with the version
    """
    valid_devices = []

    for device in VALID_DEVICES:
        if is_device_valid_for_version(device, version):
            valid_devices.append(device)

    return valid_devices


def get_device_support_info(device: str) -> dict:
    """
    Get support information for a specific device.

    Args:
        device: Device name

    Returns:
        Dictionary with 'initial' and 'final' version info
    """
    if device not in VALID_DEVICES_VERSIONS:
        return {"initial": None, "final": None}

    return VALID_DEVICES_VERSIONS[device].copy()


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
