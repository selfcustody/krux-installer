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
from serial.tools import list_ports
from src.utils.trigger import Trigger
from src.utils.selector import VALID_DEVICES


class BaseFlasher(Trigger):
    """
    Base class to flash kboot.kfpkg on devices
    """

    VALID_BOARDS = ("goE", "dan")
    VALID_BAUDRATES = (
        9600,
        19200,
        28800,
        38400,
        57600,
        76800,
        115200,
        230400,
        460800,
        576000,
        921600,
        1500000,
    )

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
        """Getter for device port system full path"""
        self.debug(f"ports::getter={self._port}")
        return self._port

    @port.setter
    def port(self, value: str):
        """Setter for available ports's full path by giving device name"""
        if value in ("amigo", "amigo_tft", "amigo_ips", "m5stickv", "bit", "cube"):
            vid = "0403"

        elif value in ("dock", "yahboom"):
            vid = "7523"

        else:
            raise ValueError(f"Device not implemented: {value}")

        self._available_ports_generator = list_ports.grep(vid)
        port = next(self._available_ports_generator)
        self._port = port.device
        self.debug(f"ports::setter={self._port}")

    @property
    def board(self) -> str:
        """Return a new instance of board"""
        self.debug(f"board::getter={self._board}")
        return self._board

    @board.setter
    def board(self, value: str):
        """Setter for board giving device name"""
        if value not in VALID_DEVICES:
            raise ValueError(f"Device not implemented: {value}")

        if value in ("amigo", "amigo_tft", "amigo_ips", "m5stickv", "bit", "cube"):
            self._board = "goE"
            self.debug(f"board::setter={self._board}")

        elif value == "dock":
            self._board = "dan"
            self.debug(f"board::setter={self._board}")

        elif value == "yahboom":
            self._board = "goE"
            self.debug(f"ports::setter={self._board}")

    @property
    def baudrate(self) -> int:
        """Getter for baudrate"""
        self.debug(f"baudrate::getter={self._baudrate}")
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value: int):
        if value in BaseFlasher.VALID_BAUDRATES:
            self.debug(f"baudrate::setter={value}")
            self._baudrate = value
        else:
            raise ValueError(f"Invalid baudrate: {str(value)}")
