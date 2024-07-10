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
import sys
import typing
from serial import Serial
from serial.serialutil import SerialException
from src.utils.flasher.base_flasher import BaseFlasher
from src.utils.kboot.build.ktool import KTool
from src.utils.selector import VALID_DEVICES


class TriggerFlasher(BaseFlasher):
    """Semi base class for Flasher and Wiper"""

    def __init__(self):
        super().__init__()
        self.ktool = KTool()

    def detect_device(self):
        """
        Detect port and board to be used
        given a valid device in VALID_DEVICES and VALID_BOARDS
        """
        for device in VALID_DEVICES:
            if device in self.firmware:
                self.info(f"Detected valid {device} for {self.firmware}")
                self.port = device
                self.board = device

    def is_port_working(self, port) -> bool:
        """Check if a port is working"""
        try:
            serialport = Serial(port)
            serialport.close()
            return True
        except SerialException:
            return False

    def process_flash(self, callback: typing.Callable):
        """
        Setup proper port, board and firmware to execute
        :attr:`KTool.process` to write proper krux
        """
        self.info(f"device: {self.port}")
        self.info(f"baudrate: {self.baudrate}")
        self.info(f"board: {self.board}")
        self.info(f"firmware: {self.firmware}")

        self.ktool.process(
            terminal=False,
            dev=self.port,
            baudrate=int(self.baudrate),
            board=self.board,
            file=self.firmware,
            callback=callback,
        )

    def process_wipe(self, callback: typing.Callable):
        """
        Setup proper port, board and firmware to execute
        :attr:`KTool.process` to erase device
        """
        self.ktool.print_callback = callback

        # Following odudex tip,
        # expand ktool arguments like
        # running it on terminal
        # in its source code, if any argument
        # is given, it will search for sys.argv arguments
        sys.argv = []
        newargs = ["-B", self.board, "-b", str(self.baudrate), "-p", self.port, "-E"]
        sys.argv.extend(newargs)
        self.ktool.process()

    def process_exception(
        self,
        exception: Exception,
        process_type: str,
        callback: typing.Callable,
    ):
        """
        Generally, Amigos have two ports. If the first fail
        use this function to process
        """
        self.info(str(exception))
        if "Greeting fail" in str(exception):
            oldport = self.port
            newport = next(self._available_ports_generator)
            msg = f"Port {oldport} didnt work, trying {newport.device}"

            # make a way to set _port without use _
            # pylint: disable=attribute-defined-outside-init
            self._port = newport.device
            self.info(str(exception))
            self.info(msg)
            proc = getattr(self, f"process_{process_type}")
            proc(callback=callback)

        else:
            raise RuntimeError(str(exception))
