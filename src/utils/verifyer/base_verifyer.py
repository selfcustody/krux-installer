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
base_verifyer.py
"""

import typing
from ..trigger import Trigger


class BaseVerifyer(Trigger):
    """Base class for verifyers"""

    def __init__(self, filename: str, read_mode: str):
        super().__init__()
        self.filename = filename
        self.read_mode = read_mode
        self.data = None

    @property
    def filename(self) -> str:
        """Getter for filename"""
        self.debug(f"filename::getter={self._filename}")
        return self._filename

    @filename.setter
    def filename(self, value: str):
        """Setter for filename"""
        self.debug(f"filename::setter={value}")
        self._filename = value

    @property
    def read_mode(self) -> str:
        """Getter for read_mode (r or rb)"""
        self.debug(f"read_mode::getter={self._read_mode}")
        return self._read_mode

    @read_mode.setter
    def read_mode(self, value: str):
        """Setter for read_mode"""
        if value in ("r", "rb"):
            self.debug(f"read_mode::setter={value}")
            self._read_mode = value
        else:
            raise ValueError(f"Invalid read_mode: {value}")

    @property
    def data(self) -> str | typing.SupportsBytes:
        """Getter for loaded data"""
        self.debug(f"data::getter={self._data}")
        return self._data

    @data.setter
    def data(self, value: str | typing.SupportsBytes):
        """Setter for data"""
        self.debug(f"data::setter={value}")
        self._data = value
