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

import io
import sys
import typing
from serial.tools import list_ports
from contextlib import redirect_stdout
from .base_flasher import BaseFlasher


# pylint: disable=unused-argument
def get_progress(file_type_str, iteration, total, suffix):
    """Default callback for flashing (repeat the one from ktool)"""
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(100 * iteration // total)
    barascii = "=" * filled_length + "-" * (100 - filled_length)
    msg = f"\r%|{barascii}| {percent}% {suffix}"
    if percent == 100:
        print()
        print(msg)
    else:
        sys.stdout.write(msg)


class Flasher(BaseFlasher):
    """
    A class to parse KTool outputs: We don't want to modify the
    KTool structure, instead, only redirect what happens in
    :attr:`KTool.process`. Following odudex approach, it uses
    :attr:`contextlib.redirect_stdout` to do this. Additionaly,
    it uses raiseup to elevate privileges to src/utils/kboot/ktool.py
    (pkexec->Linux, UAC->Windows, AppleScript->MacOS)
    """

    def configure_device(self):
        """"""
        port = ""
        
        # amigo, m5stickv
        # pylint: disable=invalid-name
        goE = list(list_ports.grep("0403"))

        # dock
        dan = list(list_ports.grep("7523"))

        if len(goE) > 0:
            self.board = "goE"
            self.port = goE[0].device
        elif len(dan) > 0:
            self.board = "dan"
            self.port = dan[0].device
        else:
            raise ValueError("No-existent valid port")
        
    def flash(self, callback: typing.Callable = get_progress):
        """
        Setup proper :attr:`dev`, :attr:`board` and :attr:file` for
        execute :attr:`KTool.process` to write proper krux firmware
        """
        try:
            self.configure_device()
            self.ktool.process(
                terminal=False,
                dev=self.port,
                baudrate=1500000,
                board=self.board,
                sram=False,
                file=self.firmware,
                callback=callback,
            )
        # pylint: disable=broad-exception-raised
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc


class Wiper(Trigger):

    def __init__(self):
        self.board = ""
    def configure_device(self):
        """"""
        port = ""
        
        # amigo, m5stickv
        # pylint: disable=invalid-name
        goE = list(list_ports.grep("0403"))

        # dock
        dan = list(list_ports.grep("7523"))

        if len(goE) > 0:
            self.board = "goE"
            self.port = goE[0].device
        elif len(dan) > 0:
            self.board = "dan"
            self.port = dan[0].device
        else:
            raise ValueError("No-existent valid port")
        
    def wipe(self, callback: typing.Callable = print):
        """Erase all data in device"""
        try:
            self.configure_device()

            buffer = io.String()
            with redirect_stdout(buffer):
                
                # As suggested by odudex
                sys.argv.extend([
                    "-B",
                    self.board,
                    "-b",
                    1500000,
                    "-E"
                ])
                self.ktool.process()
                callback(buffer.getvalue())
                
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc
