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
check_verifyer.py
"""

import os
import re
import typing
from .base_verifyer import BaseVerifyer


class CheckVerifyer(BaseVerifyer):
    """basic class for *CheckVerifyer class (do not use directly)"""

    def __init__(
        self,
        filename: str,
        read_mode: str,
        regexp: typing.Union[str, typing.Pattern[str]],
    ):
        if not re.findall(regexp, filename):
            raise ValueError(f"Invalid file: {filename} do not assert with {regexp}")

        if not os.path.exists(filename):
            raise ValueError(f"File {filename} do not exist")

        super().__init__(filename=filename, read_mode=read_mode)

    def load(self):
        """Load data in file"""
        self.debug(f"load::{self.filename}::{self.read_mode}")
        if self.read_mode == "r":
            with open(self.filename, self.read_mode, encoding="utf8") as f_data:
                self.data = f_data.read().strip()

        if self.read_mode == "rb":
            # pylint: disable=unspecified-encoding
            with open(self.filename, self.read_mode) as f_data:
                self.data = f_data.read()

    @property
    def certificate(self) -> typing.SupportsBytes:
        """Getter for certificate"""
        self.debug(f"certificate::getter={self._certificate}")
        return self._certificate

    @certificate.setter
    def certificate(self, value: typing.SupportsBytes):
        """Setter for certificate"""
        self.debug(f"certificate::setter={value}")
        self._certificate = value

    @property
    def signature(self) -> typing.SupportsBytes:
        """Getter for signature bytes"""
        self.debug(f"signature::getter={self._signature}")
        return self._signature

    @signature.setter
    def signature(self, value: typing.SupportsBytes):
        """Set the public key on X509 object"""
        self.debug(f"signature::setter={value}")
        self._signature = value
