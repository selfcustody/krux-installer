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
import requests
from kivy.cache import Cache
from .trigger import Trigger


class Selector(Trigger):
    """
    Class to select devices and firmware versions of krux
    """

    URL = "https://api.github.com/repos/selfcustody/krux/releases"
    HEADERS = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    VALID_DEVICES = ("m5stickv", "amigo_tft", "amigo_ips", "dock", "bit", "yahboom")

    def __init__(self):
        super().__init__()
        self.debug("cache::register::krux-installer={limit: 10, timeout: 60}")
        Cache.register("krux-installer", limit=10, timeout=600)

    def set_device(self, device: str):
        """
        Cache a valid device name to be memorized after,
        when it will be used to flash
        """
        if device in Selector.VALID_DEVICES:
            self.debug(f"cache::set::krux-installer::device={device}")
            Cache.append("krux-installer", "device", device)
        else:
            raise ValueError(f"Device '{device}' is not valid")

    def get_device(self) -> str:
        """
        Get the current device memorized on cache
        """
        device = Cache.get("krux-installer", "device")
        self.debug(f"cache::get::krux-installer::device={device}")
        return device

    def get_releases(self, timeout: int = 10) -> HTTPResponse:
        """
        Get the all available releases at
        https://github.com/selfcustody/krux/releases
        """
        try:
            self.debug(f"get_releases::URL={Selector.URL}")
            accept = Selector.HEADERS["Accept"]
            api = Selector.HEADERS["X-GitHub-Api-Version"]
            self.debug(f"get_releases::HEADER=Accept: {accept}")
            self.debug(f"get_releases::HEADER=X-Github-Api-Version: {api}")
            response = requests.get(
                url=Selector.URL, headers=Selector.HEADERS, timeout=timeout
            )
            response.raise_for_status()

        except requests.exceptions.Timeout as t_exc:
            raise RuntimeError(f"Timeout error: {t_exc.__cause__ }") from t_exc

        except requests.exceptions.ConnectionError as c_exc:
            raise RuntimeError(f"Connection error: {c_exc.__cause__}") from c_exc

        except requests.exceptions.HTTPError as h_exc:
            raise RuntimeError(
                f"HTTP error {response.status_code}: {h_exc.__cause__}"
            ) from h_exc

        res = response.json()
        self.debug(f"get_releases::response='{res}'")
        return res

    def get_releases_by_key(self, key: str) -> list:
        """
        Filter from a response all releases tags
        """
        response = self.get_releases()
        self.debug(f"get_releases_by_key::key={key}")

        if len(response) == 0:
            raise ValueError("Empty data")

        obj = []
        for data in response:
            if not data.get(key):
                raise KeyError(f"Invalid key: {key}")
            obj.append(data[key])

        self.debug(f"get_releases_by_key::value={obj}")
        return obj

    def set_firmware_version(self, version: str):
        """
        Cache a valid firmware version name to be memorized after,
        when it will be used to flash
        """
        valid_firmwares = self.get_releases_by_key("tag_name")

        self.debug("set_firmware_version::append=odudex/krux_binaries")
        valid_firmwares.append("odudex/krux_binaries")

        if version in valid_firmwares:
            self.debug(f"cache::append::krux-installer::firmware-version={version}")
            Cache.append("krux-installer", "firmware-version", version)
        else:
            raise ValueError(f"Firmware '{version}' is not valid")

    def get_firmware_version(self) -> str:
        """
        Get the current firmware version name memorized on cache
        """
        version = Cache.get("krux-installer", "firmware-version")
        self.debug(f"cache::get::krux-installer::version={version}")
        return version
