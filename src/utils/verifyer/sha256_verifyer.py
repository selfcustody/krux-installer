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
sha256_verifyer.py
"""

import os
import hashlib
from .base_verifyer import BaseVerifyer


class Sha256Verifyer(BaseVerifyer):
    """Verify sh256 checksum against a provided .sha256.txt file"""

    def __init__(self, filename: str):
        if os.path.exists(filename):
            super().__init__(filename, "rb")
        else:
            raise ValueError(f"File {filename} do not exist")
        self.sha256sum = None

    @property
    def sha256sum(self) -> str:
        """Getter for sha256_hash"""
        self.debug(f"sha256sum::getter={self._sha256sum}")
        return self._sha256sum

    @sha256sum.setter
    def sha256sum(self, value: str):
        """Setter for sha256_hash"""
        self.debug(f"sha256_hash::setter={value}")
        self._sha256sum = value

    def load(self):
        """Load data from"""
        sha256_hash = hashlib.sha256()

        self.debug(f"load::{self.filename}::{self.read_mode}")
        with open(self.filename, self.read_mode, encoding="utf8") as f_data:
            # Read and update hash string value in blocks of 1K
            for byte_block in iter(lambda: f_data.read(1024), b""):
                self.debug(f"load::block={byte_block}")
                sha256_hash.update(byte_block)

            self.sha256sum = sha256_hash.hexdigest()

    def verify(self, sha256sum: str) -> bool:
        """Verify self.hash against a providede sha256_hash"""
        return self.sha256sum == sha256sum
