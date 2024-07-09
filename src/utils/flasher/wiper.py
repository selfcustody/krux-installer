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
import typing
from src.utils.flasher.trigger_flasher import TriggerFlasher
from src.utils.selector import VALID_DEVICES


class Wiper(TriggerFlasher):
    """Class to wipe some specific board"""

    def wipe(self, device: str, callback: typing.Callable):
        """Detect available ports, try default erase process and
        it not work, try custom port"""
        for dev in VALID_DEVICES:
            if dev == device:
                self.info(f"Detected valid {device} to be wiped")
                self.port = device
                self.board = device

        if self.is_port_working(self.port):
            try:
                self.process_wipe(callback=callback)

            # pylint: disable=broad-exception-caught
            except Exception as exc:
                self.process_exception(
                    exception=exc, process_type="wipe", callback=callback
                )
        else:
            raise RuntimeError(f"Port not working: {self.port}")
