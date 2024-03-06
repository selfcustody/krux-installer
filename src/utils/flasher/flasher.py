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
__init__.py
"""
import sys
import typing
from .trigger_flasher import TriggerFlasher


# pylint: disable=unused-argument
def get_progress(file_type_str, iteration, total, suffix):
    """Default callback for flashing (repeat the one from ktool)"""
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(100 * iteration // total)
    barascii = "=" * filled_length + "-" * (100 - filled_length)
    msg = f"\r%|{barascii}| {percent}% {suffix}"
    if percent == 100:
        print()
        print(msg)
    else:
        sys.stdout.write(msg)


class Flasher(TriggerFlasher):
    """
    A class to parse KTool outputs: We don't want to modify the
    KTool structure, instead, only redirect what happens in
    :attr:`KTool.process`.
    """

    def __init__(self, firmware: str):
        super().__init__()
        self.firmware = firmware

    def flash(self, device: str, callback: typing.Callable = None):
        """
        Detect available ports, try default flash process and
        if not work, try custom port
        """

        port = self.get_port(device=device)
        if self.is_port_working(port.device):
            try:
                self.process_flash(port=port.device, callback=callback)

            # pylint: disable=broad-exception-caught
            except Exception as exc_info:
                self.process_exception(
                    oldport=port,
                    exc_info=exc_info,
                    process=self.process_flash,
                    callback=callback,
                )
        else:
            raise RuntimeError(f"Port not working: {port.device}")
