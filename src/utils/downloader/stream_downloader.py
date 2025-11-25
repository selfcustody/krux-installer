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
import time
import requests
from .trigger_downloader import TriggerDownloader


class StreamDownloader(TriggerDownloader):
    """
    Download files in a stream mode
    """

    def download_file_stream(self, url: str, max_retries: int = 5):
        """
        Given a :attr:`url`, download a large file in a streaming manner to given
        destination folder (:attr: `dest_dir`)

        When a chunk of received data is write to buffer, you can intercept
        some information with :attr:`on_data` as function (total_len, downloaded_len, start_time)
        until reaches the 100%.

        Then return the name
        """
        # Get the filename by url and construct the request
        # Check for any HTTPError and then process chunks of data
        retry_count = 0
        last_exception = None

        while retry_count <= max_retries:
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

                # If we get here, request was successful, break the retry loop
                break

            except requests.exceptions.Timeout as t_exc:
                raise RuntimeError(
                    f"Download timeout error: {t_exc.__cause__ }"
                ) from t_exc

            except requests.exceptions.ConnectionError as c_exc:
                raise RuntimeError(
                    f"Download connection error: {c_exc.__cause__}"
                ) from c_exc

            except requests.exceptions.HTTPError as h_exc:
                # Check if it's a 429 rate limit error
                if res.status_code == 429 and retry_count < max_retries:
                    # Exponential backoff: 2, 4, 8, 16, 32 seconds
                    wait_time = 2 ** (retry_count + 1)
                    self.debug(
                        f"Rate limited (429). Retrying in {wait_time}s "
                        f"(attempt {retry_count + 1}/{max_retries})"
                    )
                    time.sleep(wait_time)
                    retry_count += 1
                    last_exception = h_exc
                    continue
                raise RuntimeError(
                    f"HTTP error {res.status_code}: {h_exc.__cause__}"
                ) from h_exc

        # If we exhausted all retries, raise the last exception
        if retry_count > max_retries and last_exception:
            raise RuntimeError(
                f"HTTP error {res.status_code}: Failed after {max_retries} retries"
            ) from last_exception

        # get some contents to calculate the amount
        # of downloaded data
        content_len = res.headers.get("Content-Length")
        if content_len:
            self.content_len = int(content_len)
        else:
            raise RuntimeError(f"Empty Content-Length response for {url}")

        self.debug(f"download_file_stream::content_len={self.content_len}")

        # Get the chunks of bytes data
        # and pass it to a post-processing
        # method defined as `on_data`
        on_data = getattr(self, "on_data")

        for chunk in res.iter_content(chunk_size=self.chunk_size):
            self.downloaded_len += len(chunk)
            self.debug(f"download_file_stream::downloaded_len={self.downloaded_len}")

            # pylint: disable=not-callable
            on_data(data=chunk)

            # Now you can close connection
            self.debug("downloaded_file_stream::closing_connection")

        res.close()
