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
ktool_downloader.py
"""
import re
import tempfile
from platform import system, mac_ver
from .asset_downloader import AssetDownloader


class KtoolDownloader(AssetDownloader):
    """Download ktool for platform from odudex/krux_binaries"""

    def __init__(
        self,
        destdir: str = tempfile.gettempdir(),
    ):

        base_url = "https://raw.githubusercontent.com/odudex/krux_binaries/main"
        url = f"{base_url}/ktool-{self.platform}"
        super().__init__(url=url, destdir=destdir, write_mode="wb")

    @property
    # pylint: disable=too-many-return-statements
    def platform(self):
        """Getter for platform"""
        if system() == "Linux":
            return "linux"

        if system() == "Windows":
            return "win32.exe"

        if system() == "Darwin":
            version = mac_ver()
            if re.findall(r"10\..*", version):
                return "mac-10"
            if re.findall(r"11\..*", version):
                return "mac"
            if re.findall(r"12\..*", version):
                return "mac"
            if re.findall(r"13\..*", version):
                return "mac"
            if re.findall(r"14\..*", version):
                return "mac"
            raise NotImplementedError(f"Not supported mac version: {version}")

        raise NotImplementedError(f"Not supported platform: {system()}")
