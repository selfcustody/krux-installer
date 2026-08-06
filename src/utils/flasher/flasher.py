# The MIT License (MIT)

# Copyright (c) 2021-2026 Krux contributors

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

import os
from collections.abc import Callable
from src.utils.constants import (
    VALID_DEVICES,
    FirmwareIntegrityError,
    verify_firmware,
)
from src.utils.flasher.base_flasher import BaseFlasher


class Flasher(BaseFlasher):
    """
    A class to parse KTool outputs: We don't want to modify the
    KTool structure, instead, only redirect what happens in
    :attr:`KTool.process`.
    """

    def _detect_device_from_firmware(self) -> None:
        """
        Detect device type from the firmware file name and set port/board.

        Only the file name is inspected. Searching the whole path let the
        directories above it decide: under PyInstaller the path carries the
        temporary directory and the account name, so a user named 'rabbit'
        resolved to 'bit' before the device that was actually selected, which
        picks the wrong USB vendor id and board, and now also hashes the
        firmware against the wrong device's entry. get_firmware_path() always
        names the file '<device>.kfpkg', so the basename is the only part of
        the path that says anything about the device.

        Raises:
            ValueError: If the file name does not name a supported device
        """
        device = os.path.basename(self.firmware).removesuffix(".kfpkg")

        if device not in VALID_DEVICES:
            raise ValueError(f"Unknown device for firmware: {self.firmware}")

        self._device = device
        self.set_device(device)

    def _flash_with_port(self, port: str, callback: Callable) -> None:
        """
        Attempt to flash firmware using the specified port.

        The .kfpkg is re-hashed here, on the last line before KTool opens it.
        MainScreen already verified it when the Flash button was pressed, but a
        screen transition and however long the user took to react sit between
        that check and this write. Hashing again leaves no user-paced window in
        which the file unpacked to the temporary directory could be swapped.
        KTool takes a path and opens it itself, so a check adjacent to the call
        is as close as this can get — the residual microseconds are only
        reachable by something already running as the user, which is the limit
        FlashScreen states when it is done.

        Args:
            port: Serial port path
            callback: Progress callback function

        Raises:
            FirmwareIntegrityError: If the firmware no longer matches the
                SHA256 recorded at build time, or its device is unknown
        """
        if self._device is None:
            raise FirmwareIntegrityError(
                f"Could not tell which device '{self.firmware}' belongs to. "
                f"Refusing to flash unverified firmware."
            )

        verify_firmware(self._device, self.firmware)

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

        Raises:
            FirmwareIntegrityError: If the firmware fails its SHA256 check
        """
        self._detect_device_from_firmware()

        # Guard clause: check if port is working
        if not self.is_port_working(self.port):
            self._log_error(f"Port {self.port} not working")
            return

        try:
            self._flash_with_port(self.port, callback)

        # A firmware that does not match its recorded hash is not a port
        # problem: retrying on another port would flash the same altered
        # file. Let it out so FlashScreen can say what actually happened.
        except FirmwareIntegrityError:
            raise

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

            except FirmwareIntegrityError:
                raise

            except StopIteration as stop_exc:
                self._log_error(str(stop_exc))

            except Exception as gen_exc:
                self._log_error(str(gen_exc))
