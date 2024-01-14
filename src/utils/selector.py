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

import json
from urllib.request import Request, urlopen
from http.client import HTTPResponse
from kivy.cache import Cache

VALID_DEVICES = ("m5stickv", "amigo_tft", "amigo_ips", "dock", "bit", "yahboom")
VALID_VERSIONS = ["odudex/krux_binaries"]


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


def request_krux_releases() -> HTTPResponse:
    """
    Get the all available releases at
    https://github.com/selfcustody/krux/releases
    """
    url = "https://api.github.com/repos/selfcustody/krux/releases"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    req = Request(url, headers=headers)
    return urlopen(req)


def get_releases_tags(response: HTTPResponse) -> list:
    """
    Filter from a response all releases tags
    """
    data = response.read()
    return [d["tag_name"] for d in json.loads(data)]


def set_firmware_version(version: str):
    """
    Cache a valid firmware version name to be memorized after,
    when it will be used to flash
    """
    Cache.append("krux-installer", "firmware-version", version)


def get_firmware_version() -> str:
    """
    Get the current firmware version name memorized on cache
    """
    return Cache.get("krux-installer", "firmware-version")
