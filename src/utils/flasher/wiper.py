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
wiper.py
"""
import sys
from src.utils.flasher.base_flasher import BaseFlasher
from src.utils.selector import VALID_DEVICES


class Wiper(BaseFlasher):
    """Class to wipe some specific board"""

    def _detect_device(self, device: str) -> None:
        """
        Detect and validate device, then set port/board.

        Args:
            device: Device name to wipe
        """
        if device in VALID_DEVICES:
            self.info(f"Detected valid {device} to be wiped")
            self.set_device(device)

    def wipe(self, device: str) -> None:
        """
        Detect available ports, try default erase process and
        if not working, try alternative port.

        Args:
            device: Device name to wipe
        """
        self._detect_device(device)

        # Guard clause: check if port is working
        if not self.is_port_working(self.port):
            self._log_error(f"Port {self.port} not working")
            return

        try:
            sys.argv.extend(
                ["-B", self.board, "-b", str(self.baudrate), "-p", self.port, "-E"]
            )
            self.ktool.process()

        except StopIteration as stop_exc:
            self._log_error(str(stop_exc))

        # pylint: disable=broad-exception-caught
        except Exception:
            # Try alternative port on any error
            try:
                newport = next(self._available_ports_generator)
                if self.is_port_working(newport.device):
                    sys.argv = [
                        "--port",
                        newport.device,
                        "--Board",
                        self.board,
                        "--baudrate",
                        str(self.baudrate),
                        "-E",
                    ]
                    self.ktool.process()
                else:
                    self._log_error(f"Port {newport.device} not working")

            except StopIteration as stop_exc:
                self._log_error(str(stop_exc))

            except Exception as gen_exc:
                self._log_error(str(gen_exc))
