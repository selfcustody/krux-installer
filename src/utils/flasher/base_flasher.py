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
base_flasher.py
"""
import os
import sys
from serial import Serial
from serial.tools import list_ports
from ..trigger import Trigger
from ..kboot.build.ktool import KTool


class BaseFlasher(Trigger):
    """
    Base class to flash kboot.kfpkg on devices
    """

    VALID_BOARDS = ("goE", "dan")

    def __init__(self):
        super().__init__()
        self.ktool = KTool()

    def configure_device(self):
        """Configure port and board"""
        # amigo, m5stickv, yahboom
        goe_devices = list(list_ports.grep("0403"))

        # dock
        dan_devices = list(list_ports.grep("7523"))

        if len(goe_devices) > 0:
            self.board = "goE"
            self.port = goe_devices[0].device

        if len(dan_devices) > 0:
            self.board = "dan"
            self.port = dan_devices[0].device

        if len(goe_devices) == 0 and len(dan_devices) == 0:
            raise ValueError("Unavailable port: check if a valid device is connected")

    @property
    def firmware(self) -> str:
        """Getter for firmware's full path"""
        self.debug(f"firmware::getter={self._firmware}")
        return self._firmware

    @firmware.setter
    def firmware(self, value: str):
        """Setter for firmware's firmware's full path"""
        if not os.path.exists(value):
            raise ValueError(f"File do not exist: {value}")

        self.debug(f"firmware::setter={value}")
        self._firmware = value

    @property
    def port(self) -> str:
        """Getter for firmware's full path"""
        self.debug(f"port::getter={self._port}")
        return self._port

    @port.setter
    def port(self, value: str):
        """Setter for ports's full path"""
        if sys.platform in ("linux", "darwin"):
            if os.path.exists(value):
                self.debug(f"port::setter={value}")
                self._port = value
            else:
                raise OSError(f"Port do not exist: {value}")

        elif sys.platform == "win32":
            try:
                s = Serial(value)
                s.close()
                self.debug(f"port::setter={value}")
                self._port = value
            except OSError as exc:
                raise OSError(f"Unable to load port {value}: {str(exc)}") from exc
        else:
            raise EnvironmentError(f"Unsupported platform: {sys.platform}")

    @property
    def board(self) -> str:
        """Return a new instance of board"""
        self.debug(f"board::getter={self._board}")
        return self._board

    @board.setter
    def board(self, value: str):
        """Setter for board"""
        if value in BaseFlasher.VALID_BOARDS:
            self.debug(f"board::setter={value}")
            self._board = value
        else:
            raise ValueError(f"Invalid board: {value}")
