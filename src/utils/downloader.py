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
import requests


def progress_bar_cli(
    total_len: int, downloaded_len: int, start_time: int, bar_size: int = 100
):
    """
    Default :attr:`on_data` for :function:`download_zip_file`. It writes
    a progress bar, the percent of amount downloaded and the velocity
    of download.
    """
    percent = downloaded_len / total_len
    bar_amount = int(bar_size * percent)
    total_bars = "=" * bar_amount
    missing_bars = " " * (bar_size - bar_amount)
    velocity = (downloaded_len // (time.perf_counter() - start_time)) / 1000000
    percent = f"{percent * 100:.2f}"
    cli_bar = f"\r[{total_bars}{missing_bars}]"
    dld_mb = f"{downloaded_len / 1000000:.2f}"
    tot_mb = f"{total_len / 1000000:.2f}"
    sys.stdout.write(
        f"{cli_bar} {dld_mb} of {tot_mb} Mb ({percent}%) {velocity:.2f} Mb/s"
    )
    if bar_amount == bar_size:
        print()


def download_zip_file(
    url: str,
    dest_dir: str,
    chunk_size: int = 1024,
    on_data: typing.Callable = progress_bar_cli,
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
    destfile = os.path.join(dest_dir, filename)
    headers = {
        "Content-Disposition": f"attachment filename={filename}",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept-Encoding": "gzip, deflate, br",
    }

    # create a buffer to file
    zip_buffer = io.BytesIO()

    # start calculation of time to give download velocity
    start = time.perf_counter()

    # Request and check if its ok
    res = requests.get(url=url, stream=True, headers=headers, timeout=10)
    res.raise_for_status()

    # get some contents to calculate the amount
    # of downloaded data
    total_len = int(res.headers.get("Content-Length"))
    downloaded_len = 0

    # Add chunks to buffer
    for chunk in res.iter_content(chunk_size=chunk_size):
        downloaded_len += len(chunk)
        zip_buffer.write(chunk)
        on_data(total_len, downloaded_len, start)

    # close conenction
    res.close()

    # Write buffer to file
    with open(destfile, "wb") as zip_file:
        zip_file.write(zip_buffer.getvalue())
        zip_buffer.close()
        zip_file.close()

    return destfile
