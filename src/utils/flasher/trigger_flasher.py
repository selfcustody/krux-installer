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
trigger_flasher.py
"""
import re
import sys
import typing
from serial import Serial
from serial.serialutil import SerialException
from .base_flasher import BaseFlasher
from ..kboot.build.ktool import KTool


class TriggerFlasher(BaseFlasher):
    """Semi base class for Flasher and Wiper"""

    def __init__(self):
        super().__init__()
        self.ktool = KTool()

    def get_port(self, device: str):
        """Get available port from device name"""
        self.ports = device
        self.board = device
        return next(self.ports)

    def is_port_working(self, port) -> bool:
        """Check if a port is working"""
        try:
            serialport = Serial(port)
            serialport.close()
            return True
        except SerialException:
            return False

    def process_flash(self, port: str, callback: typing.Callable = None):
        """
        Setup proper port, board and firmware to execute
        :attr:`KTool.process` to write proper krux
        """
        if not callback:
            self.ktool.print_callback = print
            self.ktool.process(
                terminal=False,
                dev=port,
                baudrate=1500000,
                board=self.board,
                file=self.firmware,
            )
        else:
            self.ktool.process(
                terminal=False,
                dev=port,
                baudrate=1500000,
                board=self.board,
                file=self.firmware,
                callback=callback,
            )

    def process_wipe(self, port: str, callback: typing.Callable = None):
        """
        Setup proper port, board and firmware to execute
        :attr:`KTool.process` to erase device
        """
        if not callback:
            self.ktool.print_callback = print
        else:
            self.ktool.print_callback = callback

        sys.argv = []
        newargs = ["-B", self.board, "-b", "1500000", "-p", port, "-E"]
        sys.argv.extend(newargs)
        self.ktool.process()

    def process_exception(
        self,
        oldport: str,
        exc_info: Exception,
        process: typing.Callable = None,
        callback: typing.Callable = None,
    ):
        """
        Generally, Amigos have two ports. If the first fail
        use this function to process
        """
        if re.findall(r"Greeting fail", str(exc_info)):

            port = next(self.ports)
            msg = f"Port {oldport} didnt work, trying {port}"

            if callback:
                callback(msg)
            else:
                print(f"\033[31;1m[ERROR]\033[0m {str(exc_info)}")
                print(f"\033[33;1m[WARN]\033[0m {msg}")
                print("*")

            if process:
                process(port=port.device, callback=callback)
        else:
            if callback:
                msg = str(exc_info)
                callback(msg)
            else:
                print(f"\033[31;1m[ERROR]\033[0m {str(exc_info)}")
