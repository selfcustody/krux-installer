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

import re
import sys
import typing
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

    def flash(self, callback: typing.Callable = sys.stdout.write):
        """Execute :attr:`KTool.process` with stdout redirection"""
        if re.findall(r".*maixpy_dock/kboot.kfpkg", self.board):
            self.board = "dan"

        # pylint: disable=unused-argument
        def get_progress(file_type_str, iteration, total, suffix):
            percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
            filled_length = int(100 * iteration // total)
            barascii = "=" * filled_length + "-" * (100 - filled_length)
            msg = f"\r%|{barascii}| {percent}%% {suffix}"
            callback(msg)

        try:
            self.ktool.process(
                terminal=False,
                dev="DEFAULT",
                baudrate=1500000,
                board=self.board,
                sram=False,
                file=self.firmware,
                callback=get_progress,
            )
        except Exception as exc:
            raise exc
