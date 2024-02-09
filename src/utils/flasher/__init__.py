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

import inspect
import typing
from contextlib import redirect_stdout
from raiseup import elevate
from .base_flasher import BaseFlasher


class Flasher(BaseFlasher):
    """
    A class to parse KTool outputs: We don't want to modify the
    KTool structure, instead, only redirect what happens in
    :attr:`KTool.process`. Following odudex approach, it uses
    :attr:`contextlib.redirect_stdout` to do this. Additionaly,
    it uses raiseup to elevate privileges to src/utils/kboot/ktool.py
    (pkexec->Linux, UAC->Windows, AppleScript->MacOS)
    """

    def __init__(self, device: str, root_path: str):
        super().__init__(device=device, root_path=root_path)

    def flash(self, callback: typing.Callable = print):
        """Execute :attr:`KTool.process` with stdout redirection"""
        buffer = self.buffer
        ktool = self.ktool
        device = self.device
        with redirect_stdout(buffer):
            board = ""
            if device == "m5stickv":
                board = "goE"
            if device == "amigo_tft":
                board = "goE"
            if device == "amigo_ips":
                board = "goE"
            if device == "dock":
                board = "dan"
            if device == "bit":
                board = "goE"

            ktool_path = inspect.getfile(ktool.__class__)
            elevate(ktool_path)

            if self.has_admin_privilege():
                try:
                    self.ktool.process(
                        False, "DEFAULT", 1500000, board, file=self.full_path
                    )
                    callback(buffer.getvalue())
                except Exception as exc_info:
                    raise RuntimeError(
                        f"Unable to flash: {exc_info.__cause__}"
                    ) from exc_info
            else:
                raise RuntimeError("Do not have proper privilege to execute flash")
