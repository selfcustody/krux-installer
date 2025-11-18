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
flasher.py
"""
from collections.abc import Callable
from src.utils.selector import VALID_DEVICES
from src.utils.flasher.base_flasher import BaseFlasher


class Flasher(BaseFlasher):
    """
    A class to parse KTool outputs: We don't want to modify the
    KTool structure, instead, only redirect what happens in
    :attr:`KTool.process`.
    """

    def _detect_device_from_firmware(self) -> None:
        """Detect device type from firmware filename and set port/board"""
        for device in VALID_DEVICES:
            if device in self.firmware:
                self.set_device(device)
                return

    def _flash_with_port(self, port: str, callback: Callable) -> None:
        """
        Attempt to flash firmware using the specified port.

        Args:
            port: Serial port path
            callback: Progress callback function
        """
        self.ktool.process(
            terminal=False,
            dev=port,
            baudrate=int(self.baudrate),
            board=self.board,
            file=self.firmware,
            callback=callback,
        )

    def flash(self, callback: Callable) -> None:
        """
        Detect available ports, try default flash process and
        if not working, try alternative port.

        Args:
            callback: Progress callback function
        """
        self._detect_device_from_firmware()

        # Guard clause: check if port is working
        if not self.is_port_working(self.port):
            self._log_error(f"Port {self.port} not working")
            return

        try:
            self._flash_with_port(self.port, callback)

        except StopIteration as stop_exc:
            self._log_error(str(stop_exc))

        # pylint: disable=broad-exception-caught
        except Exception:
            # Try alternative port on any error
            try:
                newport = next(self._available_ports_generator)
                if self.is_port_working(newport.device):
                    self._flash_with_port(newport.device, callback)
                else:
                    self._log_error(f"Port {newport.device} not working")

            except StopIteration as stop_exc:
                self._log_error(str(stop_exc))

            except Exception as gen_exc:
                self._log_error(str(gen_exc))
