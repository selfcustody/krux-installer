# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

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
selector.py

Generic selector to select devices or versions
"""

from http.client import HTTPResponse
from typing import Any
import requests
from kivy.cache import Cache


VALID_DEVICES = ("m5stickv", "amigo_tft", "amigo_ips", "dock", "bit", "yahboom")


def set_device(device: str):
    """
    Cache a valid device name to be memorized after,
    when it will be used to flash
    """
    if device in VALID_DEVICES:
        Cache.append("krux-installer", "device", device)
    else:
        raise ValueError(f"Device {device} is not valid")


def get_device() -> str:
    """
    Get the current device memorized on cache
    """
    return Cache.get("krux-installer", "device")


def get_releases() -> HTTPResponse:
    """
    Get the all available releases at
    https://github.com/selfcustody/krux/releases
    """
    url = "https://api.github.com/repos/selfcustody/krux/releases"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

    except requests.exceptions.Timeout as t_exc:
        raise RuntimeError(f"Timeout error: {t_exc.__cause__ }") from t_exc

    except requests.exceptions.ConnectionError as c_exc:
        raise RuntimeError(f"Connection error: {c_exc.__cause__}") from c_exc

    except requests.exceptions.HTTPError as h_exc:
        raise RuntimeError(
            f"HTTP error {response.status_code}: {h_exc.__cause__}"
        ) from h_exc

    if response.status_code == 200:
        return response.json()

    raise RuntimeError(f"Status code: {response.status_code}")


def get_releases_by_key(response: list[dict[str, Any]], key: str) -> list:
    """
    Filter from a response all releases tags
    """
    if len(response) == 0:
        raise ValueError("Empty list")

    return [d[key] for d in response]


def set_firmware_version(version: str):
    """
    Cache a valid firmware version name to be memorized after,
    when it will be used to flash
    """
    releases = get_releases()
    valid_firmwares = get_releases_by_key(releases, "tag_name")
    valid_firmwares.append("odudex/krux_binaries")

    if version in valid_firmwares:
        Cache.append("krux-installer", "firmware-version", version)
    else:
        raise ValueError(f"Firmware '{version}' is not valid")


def get_firmware_version() -> str:
    """
    Get the current firmware version name memorized on cache
    """
    return Cache.get("krux-installer", "firmware-version")
