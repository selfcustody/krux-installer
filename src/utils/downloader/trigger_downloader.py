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
from .base_downloader import BaseDownloader


class TriggerDownloader(BaseDownloader):
    """
    Downloader with some configurations adds
    """

    def __init__(self, url: str):
        super().__init__(url=url)
        self._content_len = 0
        self._filename = ""
        self._downloaded_len = 0
        self._chunk_size = 1024

    @property
    def content_len(self) -> int:
        """Getter for the content's length of the file to be downloaded"""
        self.debug(f"content_len::getter={self._content_len}")
        return self._content_len

    @content_len.setter
    def content_len(self, value: int):
        """Setter for the content's length of the file to be downloaded"""
        self._content_len = value
        self.debug(f"content_len::setter={value}")

    @property
    def filename(self) -> str:
        """Getter for the downloaded filename"""
        self.debug(f"filename::getter={self._filename}")
        return self._filename

    @filename.setter
    def filename(self, value: str):
        """Setter for the downloaded filename"""
        self._filename = value
        self.debug(f"filename::setter={self._filename}")

    @property
    def downloaded_len(self) -> int:
        """Getter for the ammount of downloaded data"""
        self.debug(f"downloaded_len::getter={self._downloaded_len}")
        return self._downloaded_len

    @downloaded_len.setter
    def downloaded_len(self, value: int):
        """Setter for the ammount of downloaded data"""
        self._downloaded_len = value
        self.debug(f"downloaded_len:setter={self._downloaded_len}")

    @property
    def chunk_size(self) -> int:
        """Getter for the size of chunks on downloaded data"""
        self.debug(f"chunk_size::getter={self._chunk_size}")
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value: int):
        """Setter for the size of chunks on downloaded data"""
        # How to check if a given number is a power of two
        # see
        # https://stackoverflow.com/questions/57025836/how-to-check-if-a-given-number-is-a-power-of-two#57025941
        if (value & (value - 1) == 0) and value != 0:
            self.debug(f"chunk_size::setter={value}")
            self._chunk_size = value
        else:
            raise ValueError(f"{value} isnt a power of 2")
