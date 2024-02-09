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
from io import StringIO
from ..trigger import Trigger
from ..selector import VALID_DEVICES
from ..kboot.build.ktool import KTool


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

    def __init__(self, device: str, root_path: str):
        super().__init__()
        self.device = device
        self.root_path = root_path

    @property
    def device(self) -> str:
        """Getter for device to be flashed"""
        self.debug(f"device::getter={self._device}")
        return self._device

    @device.setter
    def device(self, value: str):
        """Setter for device to be flashed"""
        if value in VALID_DEVICES:
            self.debug(f"device::setter={value}")
            self._device = value
        else:
            raise ValueError(f"Invalid device: {value}")

    @property
    def root_path(self) -> str:
        """Getter for root_path's filename"""
        self.debug(f"root_path::getter={self._root_path}")
        return self._root_path

    @root_path.setter
    def root_path(self, value: str):
        """Setter for firmware's root_path's/full_path"""
        full_path = os.path.join(value, f"maixpy_{self.device}", "kboot.kfpkg")

        if not os.path.exists(value):
            raise ValueError(f"Directory {value} do not exist")

        if not os.path.exists(full_path):
            raise ValueError(f"File {full_path} do not exist")

        self.debug(f"root_path::setter={value}")
        self._root_path = value

        self.debug(f"full_path::setter={full_path}")
        self._full_path = full_path

    @property
    def full_path(self) -> str:
        """Getter for firmware's full_path's"""
        self.debug(f"root_path::getter={self._full_path}")
        return self._full_path

    @property
    def ktool(self) -> KTool:
        """Return a new instance of ktool"""
        ktool = KTool()
        self.debug(f"ktool::getter={ktool}")
        return ktool

    @property
    def buffer(self) -> StringIO:
        """Return a new instance of StringIO"""
        buffer = StringIO()
        self.debug(f"buffer::getter={buffer}")
        return buffer

    @property
    def has_admin_privilege(self) -> bool:
        """Getter for has_admin_privilege"""
        is_root = os.getuid() == 0
        self.debug(f"has_admin_privilege::getter={is_root}")
        return is_root
