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
import tempfile
import typing
from zipfile import ZipFile, BadZipFile
from ..verifyer.check_verifyer import CheckVerifyer


class BaseUnzip(CheckVerifyer):
    """Base class to unzip files"""

    def __init__(
        self,
        filename: str,
        members: typing.List[str],
        output: str = tempfile.gettempdir(),
    ):
        super().__init__(filename=filename, read_mode="r", regexp=r".*\.zip")

        # make an unordered list of members
        self.members = members
        self.output = output

    @property
    def members(self) -> typing.List[str]:
        """Getter for the name of members files to be extracted from zip"""
        self.debug(f"members::getter={self._filename}")
        return list(self._members)

    @members.setter
    def members(self, value: typing.List[str]):
        """Setter for the name of file to be extracted"""
        if len(value) > 0:
            self.debug(f"members::setter={value}")
            self._members = set(value)
        else:
            raise ValueError("Members cannot be empty")

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

    @staticmethod
    def sanitized_base_name(filename):
        """Extract the name of zip release without folder tree and .zip extension"""
        base_name = os.path.basename(filename)
        return base_name.replace(".zip", "")

    def load(self):
        """Extract from given zip file only the ones that was defined as members"""
        try:
            self.debug(f"load::opening={self.filename}")
            with ZipFile(self.filename, self.read_mode) as zip_obj:
                namelist = set(zip_obj.namelist())
                self.debug(f"load::namelist={namelist}")
                for name in namelist:
                    if name in self.members:
                        self.debug(f"load::extract::{self.filename}={name}")
                        zip_obj.extract(name, path=self.output)

        except BadZipFile as exc_info:
            raise RuntimeError(
                f"Cannot open {self.filename}: {exc_info.__cause__}"
            ) from exc_info
