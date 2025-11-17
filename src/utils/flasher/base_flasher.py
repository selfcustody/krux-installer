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
from serial import Serial
from serial.serialutil import SerialException
from serial.tools import list_ports
from src.utils.trigger import Trigger
from src.utils.kboot.build.ktool import KTool


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
        400000,
        460800,
        576000,
        921600,
        1500000,
    )

    # Device to VID mapping
    DEVICE_VID_MAP = {
        "amigo": "0403",
        "amigo_tft": "0403",
        "amigo_ips": "0403",
        "m5stickv": "0403",
        "bit": "0403",
        "cube": "0403",
        "dock": "7523",
        "yahboom": "7523",
        "wonder_mv": "7523",
        "embed_fire": "7523",
        "tzt": "55d3",
    }

    # Device to board mapping
    DEVICE_BOARD_MAP = {
        "amigo": "goE",
        "amigo_tft": "goE",
        "amigo_ips": "goE",
        "m5stickv": "goE",
        "bit": "goE",
        "yahboom": "goE",
        "cube": "goE",
        "dock": "dan",
        "wonder_mv": "dan",
        "tzt": "dan",
        "embed_fire": "dan",
    }

    def __init__(self):
        super().__init__()
        self.ktool = KTool()
        self.stop_thread = False
        self.print_callback = None
        self._firmware = None
        self._port = None
        self._board = None
        self._baudrate = None

    @property
    def firmware(self) -> str:
        """Firmware file path with validation"""
        return self._firmware

    @firmware.setter
    def firmware(self, value: str):
        """Set firmware file path with validation"""
        if not os.path.exists(value):
            raise ValueError(f"File does not exist: {value}")
        self.debug(f"firmware::setter={value}")
        self._firmware = value

    @property
    def port(self) -> str:
        """Device port path"""
        return self._port

    @port.setter
    def port(self, device: str):
        """Set port by device name (e.g., 'amigo', 'dock', 'tzt')"""
        if (vid := self.DEVICE_VID_MAP.get(device)) is None:
            raise ValueError(f"Device not implemented: {device}")

        self._available_ports_generator = list_ports.grep(vid)
        self._port = next(self._available_ports_generator).device
        self.debug(f"port::setter={self._port} (from device {device})")

    @property
    def board(self) -> str:
        """Board type ('goE' or 'dan')"""
        return self._board

    @board.setter
    def board(self, device: str):
        """Set board by device name (e.g., 'amigo', 'dock')"""
        if (board := self.DEVICE_BOARD_MAP.get(device)) is None:
            raise ValueError(f"Device not implemented: {device}")
        self._board = board
        self.debug(f"board::setter={self._board} (from device {device})")

    @property
    def baudrate(self) -> int:
        """Baudrate with validation"""
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value: int):
        """Set baudrate with validation"""
        if value not in self.VALID_BAUDRATES:
            raise ValueError(f"Invalid baudrate: {value}")
        self.debug(f"baudrate::setter={value}")
        self._baudrate = value

    def set_device(self, device: str) -> None:
        """
        Set both port and board for a given device name.
        Also enforces device-specific constraints (e.g., baudrate limits).

        Args:
            device: Device name (e.g., 'amigo', 'dock', 'tzt')
        """
        self.port = device
        self.board = device

        # Enforce baudrate limit for embed_fire
        if device == "embed_fire" and self.baudrate and self.baudrate > 400000:
            self.debug(
                f"baudrate {self.baudrate} exceeds embed_fire limit, capping at 400000"
            )
            self.baudrate = 400000

    def _log_error(self, message: str) -> None:
        """
        Log an error message using ktool's logging mechanism.

        Args:
            message: Error message to log
        """
        self.ktool.__class__.log(message)

    def is_port_working(self, port: str) -> bool:
        """Check if a port is working"""
        try:
            with Serial(port):
                pass  # Connection successful
            return True
        except SerialException:
            return False
