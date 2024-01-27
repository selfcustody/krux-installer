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
stream_downloader.py
"""
import os
import sys
import typing
import requests
from .trigger_downloader import TriggerDownloader


class StreamDownloader(TriggerDownloader):
    """
    Download files in a stream mode
    """

    def __init__(self):
        super().__init__()
        self.content_len = 0
        self.filename = None
        self.downloaded_len = 0
        self.chunk_size = 1024
        self.progress_bar_size = 128
        self.on_data = self.progress_bar_cli

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
        self._chunk_size = value
        self.debug(f"chunk_size::setter={self._chunk_size}")

    @property
    def progress_bar_size(self) -> int:
        """Getter for the size of progress_bar_cli"""
        self.debug(f"progress_bar_size::getter={self._progress_bar_size}")
        return self._progress_bar_size

    @progress_bar_size.setter
    def progress_bar_size(self, value: int):
        """Setter for the size of progress_bar_cli"""
        self._progress_bar_size = value
        self.debug(f"progress_bar_size::setter={self._progress_bar_size}")

    @property
    def on_data(self) -> typing.Callable:
        """Getter for callback to be used in each increment of downloaded stream"""
        self.debug(f"on_data::getter={self._on_data}")
        return self._on_data

    @on_data.setter
    def on_data(self, value: typing.Callable):
        """Setter for the callback to be used in each increment of downloaded stream"""
        self._on_data = value
        self.debug(f"on_data::setter={value}")

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
        percent = f"{percent * 100:.2f}"
        cli_bar = f"\r[{total_bars}{missing_bars}]"
        dld_mb = f"{self.downloaded_len / 1000000:.2f}"
        tot_mb = f"{self.content_len / 1000000:.2f}"
        sys.stdout.write(f"{cli_bar} {dld_mb} of {tot_mb} Mb ({percent}%)")
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

        # Add chunks to BufferError
        for chunk in res.iter_content(chunk_size=self.chunk_size):
            if self._on_data is not None:
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
