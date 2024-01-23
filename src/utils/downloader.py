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
downloader.py

some functions to mange download process
"""
import os
import io
import sys
import time
import typing
import tempfile
import requests
from .trigger import Trigger


class StreamDownloader(Trigger):
    """
    Download files in a stream mode
    """

    buffer: typing.SupportsBytes = io.BytesIO()
    """Buffer to store streamed data"""

    filename: str = None
    """Filename based on a given url"""

    content_len: int = 0
    """The length of streamed data"""

    downloaded_len: int = 0
    """The amount of downloaded data by increments of chunk_size"""

    started_at: int = 0
    """The start time of stream"""

    on_data: typing.Callable
    """The callback to be used in each increment of downloaded stream"""

    chunk_size: int = 1024
    """The increment size of data"""

    progress_bar_size = 128
    """The size of utf8 bar in CLI mode"""

    def __init__(self):
        super().__init__()
        self.set_on_data(self.progress_bar_size)

    def set_on_data(self, callback: typing.Callable):
        """
        Set callback to handle stream iteration
        """
        self.debug("set_on_data::on_data")
        self.on_data = callback

    def progress_bar_cli(
        self,
        data: bytes,  # pylint: disable=unused-argument
    ):
        """
        Default :attr:`on_data` for :function:`download_zip_file`. It writes
        a progress bar, the percent of amount downloaded and the velocity
        of download.
        """
        percent = self.downloaded_len / self.content_len
        bar_amount = int(self.progress_bar_size * percent)
        total_bars = "=" * bar_amount
        missing_bars = " " * (self.progress_bar_size - bar_amount)
        velocity = (
            self.downloaded_len // (time.perf_counter() - self.started_at)
        ) / 1000000
        percent = f"{percent * 100:.2f}"
        cli_bar = f"\r[{total_bars}{missing_bars}]"
        dld_mb = f"{self.downloaded_len / 1000000:.2f}"
        tot_mb = f"{self.content_len / 1000000:.2f}"
        sys.stdout.write(
            f"{cli_bar} {dld_mb} of {tot_mb} Mb ({percent}%) {velocity:.2f} Mb/s"
        )
        if bar_amount == self.progress_bar_size:
            print()

    def download_file_stream(self, url: str) -> str:
        """
        Given a :attr:`url`, download a large file in a streaming manner to given
        destination folder (:attr:`dest_dir`)

        When a chunk of received data is write to buffer, you can intercept
        some information with :attr:`on_data` as function (total_len, downloaded_len, start_time)
        until reaches the 100%.

        Then return the name
        """
        try:
            self.filename = os.path.basename(url)
            self.debug(f"download_file_stream::filename={self.filename}")

            headers = {
                "Content-Disposition": f"attachment filename={self.filename}",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Accept-Encoding": "gzip, deflate, br",
            }
            self.debug(
                "download_file_stream::requests.get=< url: "
                + f"{url}, stream: True, headers: {headers}, timeout: 30 >"
            )
            res = requests.get(url=url, stream=True, headers=headers, timeout=30)

            self.debug("download_file_stream::raise_for_status")
            res.raise_for_status()

        except requests.exceptions.Timeout as t_exc:
            raise RuntimeError(f"Timeout error: {t_exc.__cause__ }") from t_exc

        except requests.exceptions.ConnectionError as c_exc:
            raise RuntimeError(f"Connection error: {c_exc.__cause__}") from c_exc

        except requests.exceptions.HTTPError as h_exc:
            raise RuntimeError(
                f"HTTP error {res.status_code}: {h_exc.__cause__}"
            ) from h_exc

        # get some contents to calculate the amount
        # of downloaded data
        self.content_len = int(res.headers.get("Content-Length"))
        self.debug(f"download_file_stream::content_len={self.content_len}")

        # start to count time if using
        # sortedme type of deownload's velocity meter
        self.started_at = time.perf_counter()
        self.debug(f"download_file_stream::started_at={self.started_at}")

        # Add chunks to BufferError
        for chunk in res.iter_content(chunk_size=self.chunk_size):
            if self.on_data is not None:
                self.downloaded_len += len(chunk)
                self.debug(
                    f"download_file_stream::downloaded_len={self.downloaded_len}"
                )
                self.on_data(data=chunk)
            else:
                raise NotImplementedError(
                    "on_data function not implemented to callback data"
                )

        self.debug("downloaded_file_stream::closing_connection")
        res.close()


class StreamDownloaderZipRelease(StreamDownloader):
    """Subclass of :class:`StreamDownloader` for versioned zip releases"""

    url: str = None
    """The url of version to be downloaded"""

    destdir: str = None
    """Destination dir where the downloaded file will be placed"""

    _callback_on_write_to_buffer: typing.Callable = None
    """The callback to execute after writing to buffer"""

    def __init__(self, version: str, destdir: str = tempfile.gettempdir()):
        super().__init__()
        self.set_destdir(destdir)
        self.set_url(version)
        self.set_on_data(self.write_to_buffer)

    def set_destdir(self, destdir):
        """
        Set the destination on system of downloaded stream
        """
        self.destdir = destdir
        self.debug(f"set_destdir::destdir={self.destdir}")

    def set_url(self, version: str):
        """
        Set the URL of the desired asset to be downloaded
        """
        self.url = "".join(
            [
                "https://github.com/selfcustody/krux/releases/download/",
                f"{version}/krux-{version}.zip",
            ]
        )
        self.debug(f"set_url::url={self.url}")

    def write_to_buffer(self, data: bytes):
        """
        Callback to be used when writing streamed data to buffer
        and pass the same data to :attr:`_callback_on_write_to_buffer`
        """
        if self._callback_on_write_to_buffer:
            self.buffer.write(data)
            self._callback_on_write_to_buffer(data)
        else:
            raise NotImplementedError("Use 'set_callback_on_write_to_buffer'")

    def set_on_write_to_buffer(self, callback: typing.Callable):
        """
        Set the callback to execute after writed to buffer
        """
        self.debug("set_callback_on_write_to_buffer::_calback_on_write_to_buffer")
        self._callback_on_write_to_buffer = callback

    def download(self) -> str:
        """
        Download some zip release given its version and put it
        on a destination directory (default: OS temporary dir)
        """
        self.download_file_stream(url=self.url)

        destfile = os.path.join(self.destdir, self.filename)
        self.debug(f"download::destfile={destfile}")

        with open(destfile, "wb") as zip_file:
            self.debug(f"download::zip_file.write={self.buffer.getvalue()}")
            zip_file.write(self.buffer.getvalue())

        return destfile
