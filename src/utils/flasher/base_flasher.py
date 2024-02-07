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
import re
import tempfile
import typing
from ..trigger import Trigger
from ..selector import Selector.VALID_DEVICES

            
class BaseFlasher(Trigger):
    """
    Base class to flash kboot.kfpkg on devices

    Args:
    -----
        device: str ->
            One of :attr:`selector.Selector.VALID_DEVICES`
    
        on_print_progress_bar: typing.Callable ->
            a callback(prefix: str, percent: float, suffix: str)
    """

    def __init__(
        self,
        device: str,
        on_log: typing.Callable
    ):
        super().__init__()
        self.device = device
        self.on_log = on_log
        

    @property
    def device(self) -> str:
        """Getter for device to be flashed"""
        self.debug(f"device::getter={self._device}")

    @device.setter(self, value: str):
        """Setter for device to be flashed"""
        if device in VALID_DEVICES:
            self.debug(f"device::setter={value}")
            self._device = value
        else:
            raise ValueError(f"Invalid device: {value}")

    @property
    def on_log(self) -> typing.Callable:
        """Getter for callback on any :attr:`KTool.log`"""
        self.debug(f"on_print_progress_bar::getter={self._on_log}")
        return self._on_log

    @on_log.setter
    def on_log(self, value: typing.Callable):
        """Setter for callback atr :attr:`KTool.log` """
        self.debug(f"on_log:setter={value}")
        self._on_log = value

