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
beta_downloader.py
"""
import tempfile
from .asset_downloader import AssetDownloader


class BetaDownloader(AssetDownloader):
    """Download beta assets from odudex/krux_binaries"""

    VALID_DEVICES = (
        "m5stickv",
        "amigo",
        "dock",
        "bit",
        "yahboom",
        "cube",
        "wonder_mv",
        "tzt",
        "embed_fire",
    )

    VALID_BINARY_TYPES = ("firmware.bin", "kboot.kfpkg")

    def __init__(
        self,
        device: str,
        binary_type: str,
        destdir: str = tempfile.gettempdir(),
    ):
        base_url = "https://raw.githubusercontent.com/odudex/krux_binaries/main"
        url = f"{base_url}/maixpy_{device}/{binary_type}"
        super().__init__(url=url, destdir=destdir, write_mode="wb")
        self.device = device
        self.binary_type = binary_type

    @property
    def device(self):
        """Getter for the device of beta version"""
        self.debug(f"device::getter={self._device}")
        return self._device

    @device.setter
    def device(self, value: str):
        """Setter for the device of beta version"""
        if value in BetaDownloader.VALID_DEVICES:
            self.debug(f"device::setter={value}")
            self._device = value
        else:
            raise ValueError(f"Invalid device {value}")

    @property
    def binary_type(self):
        """Getter for the binary_type of beta version to be downloaded (firmware or kboot)"""
        self.debug(f"binary_type::getter={self._binary_type}")
        return self._binary_type

    @binary_type.setter
    def binary_type(self, value: str):
        """Setter for the binary_type of beta version to be downloaded (firmware or kboot)"""
        if value in BetaDownloader.VALID_BINARY_TYPES:
            self.debug(f"binary::setter={value}")
            self._binary_type = value
        else:
            raise ValueError(f"Invalid binary_type {value}")
