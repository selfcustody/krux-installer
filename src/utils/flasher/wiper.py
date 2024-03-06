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
from .trigger_flasher import TriggerFlasher


class Wiper(TriggerFlasher):
    """Class to wipe some specific board"""

    def wipe(self, device: str, callback: typing.Callable = None):
        """Erase all data in device"""

        port = self.get_port(device=device)
        if self.is_port_working(port.device):
            try:
                self.process_wipe(port=port.device, callback=callback)

            # pylint: disable=broad-exception-caught
            except Exception as exc_info:
                self.process_exception(
                    oldport=port,
                    exc_info=exc_info,
                    process=self.process_wipe,
                    callback=callback,
                )
        else:
            raise RuntimeError(f"Port not working: {port.device}")
