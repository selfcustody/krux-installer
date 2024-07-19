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
import typing
from src.utils.selector import VALID_DEVICES
from src.utils.flasher.base_flasher import BaseFlasher

# Example of parsing progress
# def get_progress(file_type_str, iteration, total, suffix):
#    """Default callback for flashing (repeat the one from ktool)"""
#    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
#    filled_length = int(100 * iteration // total)
#    barascii = "=" * filled_length + "-" * (100 - filled_length)
#    msg = f"\r%|{barascii}| {percent}% {suffix}"
#    if percent == 100:
#        print()
#        print(msg)
#    else:
#        sys.stdout.write(msg)


class Flasher(BaseFlasher):
    """
    A class to parse KTool outputs: We don't want to modify the
    KTool structure, instead, only redirect what happens in
    :attr:`KTool.process`.
    """

    def flash(self, callback: typing.Callable):
        """
        Detect available ports, try default flash process and
        if not work, try custom port
        """
        for device in VALID_DEVICES:
            if device in self.firmware:
                self.port = device
                self.board = device

        if self.is_port_working(self.port):
            try:
                self.ktool.process(
                    terminal=False,
                    dev=self.port,
                    baudrate=int(self.baudrate),
                    board=self.board,
                    file=self.firmware,
                    callback=callback,
                )

            # pylint: disable=broad-exception-caught
            except Exception as exc:
                self.ktool.__class__.log(f"{str(exc)} for {self.port}")
                self.ktool.__class__.log("")

                try:
                    newport = next(self._available_ports_generator)
                    if self.is_port_working(newport.device):
                        self.ktool.process(
                            terminal=False,
                            dev=newport.device,
                            baudrate=int(self.baudrate),
                            board=self.board,
                            file=self.firmware,
                            callback=callback,
                        )

                    else:
                        exc = RuntimeError(f"Port {newport.device} not working")
                        self.ktool.__class__.log(str(exc))

                except StopIteration as stop_exc:
                    self.ktool.__class__.log(str(stop_exc))

        else:
            exc = RuntimeError(f"Port {self.port} not working")
            self.ktool.__class__.log(str(exc))
