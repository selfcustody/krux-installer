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
asset_downloader.py
"""
import os
import typing
from .stream_downloader import StreamDownloader


class AssetDownloader(StreamDownloader):
    """
    Subclass of :class:`StreamDownloader` for versioned asset releases.
    """

    def __init__(self, url: str, destdir: str, write_mode: str):
        super().__init__(url=url)
        self.destdir = destdir
        self.on_data = self.write_to_buffer
        self.on_write_to_buffer = self.progress_bar
        self.write_mode = write_mode

    @property
    def destdir(self) -> str:
        """Getter for destination dir where the downloaded file will be placed"""
        self.debug(f"destdir::getter={self._destdir}")
        return self._destdir

    @destdir.setter
    def destdir(self, value):
        """Setter for destination dir where the downloaded file will be placed"""
        self.debug(f"destdir::setter={value}")
        if not os.path.exists(value):
            os.makedirs(value, exist_ok=True)

        self._destdir = value

    @property
    def on_write_to_buffer(self):
        """
        Getter for callback to be executed after a data is wrote to buffer
        """
        self.debug("on_write_to_buffer::getter")
        return self._on_write_to_buffer

    @on_write_to_buffer.setter
    def on_write_to_buffer(self, value: typing.Callable):
        """
        Setter for callback to be executed after a data is wrote to buffer
        """
        self.debug("on_write_to_buffer::setter")
        self._on_write_to_buffer = value

    @property
    def write_mode(self) -> str:
        """Getter for write mode ('wb' or 'w')"""
        self.debug(f"write_mode::getter={self._write_mode}")
        return self._write_mode

    @write_mode.setter
    def write_mode(self, value: str):
        """Setter for write mode ('wb' or 'w')"""
        if value in ("w", "wb"):
            self.debug(f"write_mode::setter={value}")
            self._write_mode = value
        else:
            raise ValueError(f"Write Mode '{value}' not supported")

    def write_to_buffer(self, data: bytes):
        """
        Callback to be used when writing streamed data to buffer
        and pass the same data to :attr:`_callback_on_write_to_buffer`
        """
        if self.on_write_to_buffer is not None:
            self.debug(f"write_to_buffer::buffer::write={data}")
            self.buffer.write(data)

            self.debug("write_to_buffer::_callback_on_write_to_buffer")
            self.on_write_to_buffer(data)
        else:
            raise NotImplementedError("on_write_to_buffer bound method not set")

    def download(self) -> str:
        """
        Download some zip release given its version and put it
        on a destination directory (default: OS temporary dir)
        """
        self.download_file_stream(url=self.url)

        destfile = os.path.join(self.destdir, self.filename)
        self.debug(f"download::destfile={destfile}")

        self.debug(f"download::write::{self.write_mode}={self.buffer.getvalue()}")
        if self.write_mode == "wb":
            # pylint: disable=unspecified-encoding
            with open(destfile, self.write_mode) as file:
                file.write(self.buffer.getvalue())

        if self._write_mode == "w":
            with open(destfile, self.write_mode, encoding="utf8") as file:
                value = self.buffer.getvalue()
                text = value.decode("utf8")
                file.write(text)

        return destfile
