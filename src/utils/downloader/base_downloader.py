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
trigger_downloader.py
"""

import re
from io import BytesIO
from ..trigger import Trigger


class BaseDownloader(Trigger):
    """
    Base class for downloader
    """

    REGEXP = r"https:\/\/(raw\.)?github(usercontent)?\.com\/(selfcustody|odudex)\/krux(\_binaries)?"

    def __init__(self, url: str):
        super().__init__()
        self._buffer = BytesIO()
        self.url = url

    @property
    def buffer(self) -> BytesIO:
        """Getter for the buffer of the file to be downloaded"""
        self.debug(f"buffer::getter={self._buffer}")
        return self._buffer

    @property
    def url(self) -> str:
        """The asset's url to be downloaded"""
        self.debug(f"url::getter={self._url}")
        return self._url

    @url.setter
    def url(self, value: str):
        """The asset's url to be downloaded"""
        if re.findall(BaseDownloader.REGEXP, value):
            self.debug(f"url::setter={value}")
            self._url = value
        else:
            raise ValueError(f"Invalid url: {value}")
