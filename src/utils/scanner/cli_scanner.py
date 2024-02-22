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
cli_scanner.py
"""

import typing
from pyzbar.pyzbar import decode, PyZbarError
from .base_scanner import BaseScanner


class CliScanner(BaseScanner):
    """Scanner for krux-installer as CLI"""

    def __init__(self):
        super().__init__(capture_dev=0)

    def scan(self) -> typing.List:
        """Open scan window and detect/decode a QRCode"""

        while True:
            try:
                _ret, frame = self.video_capture.read()
                qrcode = decode(frame)
            except PyZbarError as exc_info:
                raise RuntimeError(exc_info.__cause__) from exc_info
            except Exception as exc_info:
                raise RuntimeError(exc_info.__cause__) from exc_info

            if qrcode:
                break

            CliScanner.show_freeze_image(frame)

            if CliScanner.on_click_quit():
                break

        self.close_cli_capture()
        return qrcode[0].data
