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


def progress_bar_cli(
    data: bytes,  # pylint: disable=unused-argument
    content_len: int,
    downloaded_len: int,
    started_at: int,
    bar_size: int = 100,
):
    """
    Default :attr:`on_data` for :function:`download_zip_file`. It writes
    a progress bar, the percent of amount downloaded and the velocity
    of download.
    """
    percent = downloaded_len / content_len
    bar_amount = int(bar_size * percent)
    total_bars = "=" * bar_amount
    missing_bars = " " * (bar_size - bar_amount)
    velocity = (downloaded_len // (time.perf_counter() - started_at)) / 1000000
    percent = f"{percent * 100:.2f}"
    cli_bar = f"\r[{total_bars}{missing_bars}]"
    dld_mb = f"{downloaded_len / 1000000:.2f}"
    tot_mb = f"{content_len / 1000000:.2f}"
    sys.stdout.write(
        f"{cli_bar} {dld_mb} of {tot_mb} Mb ({percent}%) {velocity:.2f} Mb/s"
    )
    if bar_amount == bar_size:
        print()


def download_file_stream(
    url: str, chunk_size: int = 1024, on_data: typing.Callable = progress_bar_cli
) -> str:
    """
    Given a :attr:`url`, download a large file in a streaming manner to given
    destination folder (:attr:`dest_dir`)

    When a chunk of received data is write to buffer, you can intercept
    some information with :attr:`on_data` as function (total_len, downloaded_len, start_time)
    until reaches the 100%.

    Then return the name
    """
    filename = os.path.basename(url)
    headers = {
        "Content-Disposition": f"attachment filename={filename}",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept-Encoding": "gzip, deflate, br",
    }

    # Request and check if its ok
    try:
        res = requests.get(url=url, stream=True, headers=headers, timeout=10)
        res.raise_for_status()

    except requests.exceptions.Timeout as t_exc:
        raise RuntimeError(f"Timeout error: {t_exc.__cause__ }") from t_exc

    except requests.exceptions.ConnectionError as c_exc:
        raise RuntimeError(f"Connection error: {c_exc.__cause__}") from c_exc

    except requests.exceptions.HTTPError as h_exc:
        raise RuntimeError(
            f"HTTP error {res.status_code}: {h_exc.__cause__}"
        ) from h_exc

    if res.status_code == 200:
        start = time.perf_counter()

        # get some contents to calculate the amount
        # of downloaded data
        total_len = int(res.headers.get("Content-Length"))
        downloaded_len = 0

        # Add chunks to BufferError
        for chunk in res.iter_content(chunk_size=chunk_size):
            downloaded_len += len(chunk)
            on_data(
                data=chunk,
                content_len=total_len,
                downloaded_len=downloaded_len,
                started_at=start,
            )
        res.close()


def download_zip_release(
    version: str,
    dest_dir: str = tempfile.gettempdir(),
    on_data: typing.Callable = progress_bar_cli,
) -> str:
    """
    Download some zip release given its version and put it
    on a destination directory (default: OS temporary dir)
    """
    url = f"https://github.com/selfcustody/krux/releases/download/v23.09.1/krux-{version}.zip"
    filename = os.path.basename(url)
    destfile = os.path.join(dest_dir, filename)

    # create a buffer to file
    with io.BytesIO() as zip_buffer:

        def write_to_buffer(data, content_len, downloaded_len, started_at):
            zip_buffer.write(data)
            on_data(data, content_len, downloaded_len, started_at)

        download_file_stream(url=url, on_data=write_to_buffer)

        # Write buffer to file
        with open(destfile, "wb") as zip_file:
            zip_file.write(zip_buffer.getvalue())

    return destfile
