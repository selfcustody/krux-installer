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
base_unzip.py
"""
import os
import typing
from zipfile import (
    ZipFile,
    BadZipFile
)
from ..verifyer.base_verifyer import BaseVerifyer


class BaseUnzip(BaseVerifyer):
    """Base class to unzip files"""

    def __init__(self, filename: str, members: typing.List[str], output=str):
        super().__init__(filename=filename, read_mode="rb", regexp=r".*\.zip")
        self.members = members
        self.output = output

    @property
    def members(self) -> typing.List[str]:
        """Getter for the name of members files to be extracted from zip"""
        self.debug(f"members::getter={self._filename}")
        return self._members

    @members.setter
    def members(self, value: typing.List[str]):
        """Setter for the name of file to be extracted"""
        self.debug(f"members::setter={value}")
        self._members = value

    @property
    def output(self) -> str:
        """Getter for the path where extracted files will be placed"""
        self.debug(f"output::getter={self._output}")
        return self._output

    @output.setter
    def output(self, value: str):
        """Setter for the path where extracted files will be placed"""
        if os.path.exists(value):
            self.debug(f"output::setter={value}")
            self._output = value
        else:
            raise ValueError(f"Given path not exist: {value}")

    def extract(self):
        """Extract from given zip file only the ones that was defined as members"""
        try:
            with ZipFile(self.filename, self.read_mode) as zipObj:
                namelist = zipObj.namelist()
                for name in namelist:
                    if name in self.members:
                        self.debug(f"extract::{self.filename}={name}")
                        zipObj.extract(name, path=self.output)
                    else:
                        self.debug(f"extract::{self.filename}::skip={name}")
                        
        except BadZipFile as exc_info:
            raise RuntimeError(f"Cannot open {self.filename}: {exc_info.__cause__}")
