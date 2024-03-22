# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

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
base_signer.py
"""
import os
import re
import typing
from ..trigger import Trigger


class BaseSigner(Trigger):
    """
    BaseSigner
    """

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    @property
    def filename(self) -> str:
        """Getter for filename"""
        self.debug(f"filename::getter={self._filename}")
        return self._filename

    @filename.setter
    def filename(self, value: str):
        """Setter for filename"""
        if os.path.exists(value):
            self.debug(f"filename::setter={value}")
            self._filename = value
        else:
            raise ValueError(f"{value} do not exists")

    @property
    def filehash(self) -> str:
        """Getter for filehash"""
        self.debug(f"filehash::getter={self._filehash}")
        return self._filehash

    @filehash.setter
    def filehash(self, value: str):
        """Setter for filehash"""
        if re.findall(r"[a-fA-F0-9]{64}", value):
            self.debug(f"filehash::setter={value}")
            self._filehash = value
        else:
            raise ValueError(f"Invalid hash: {value}")

    @property
    def signature(self) -> typing.SupportsBytes:
        """Getter for signature"""
        self.debug(f"signature::getter={self._signature}")
        return self._signature

    @signature.setter
    def signature(self, value: typing.SupportsBytes):
        """Setter for signature"""
        self.debug(f"signature::setter={value}")
        self._signature = value

    @property
    def pubkey(self) -> str:
        """Getter for public key certificate"""
        self.debug(f"pubkey::getter={self._signature}")
        return self._pubkey

    @pubkey.setter
    def pubkey(self, value: typing.SupportsBytes):
        """Setter for public key certificate"""
        self.debug(f"pubkey::setter={value}")
        self._pubkey = value
