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
__init__.py
"""

import typing
from contextlib import redirect_stdout
from .base_flasher import BaseFlasher


class Flasher(BaseFlasher):
    """
    A class to parse KTool outputs

    We don't want to modify the KTool structure,
    instead, only redirect what happens in :attr:`KTool.process`.

    Following odudex approach, it uses :attr:`contextlib.redirect_stdout`
    to do this.

    TODO: add sudoer GUI
    """

    def __init__(self, device: str, firmware: str):
        super().__init__(device=device, firmware=firmware)

    def flash(self, callback: typing.Callable = print):
        """Execute :attr:`KTool.process` with stdout redirection"""
        buffer = self.buffer
        with redirect_stdout(buffer):
            board = ""
            if self.device == "m5stickv":
                board = "goE"
            if self.device == "amigo_tft":
                board = "goE"
            if self.device == "amigo_ips":
                board = "goE"
            if self.device == "dock":
                board = "dan"
            if self.device == "bit":
                board = "goE"

            self.ktool.process(False, "DEFAULT", 1500000, board, file=self.firmware)
            callback(buffer.getvalue())
