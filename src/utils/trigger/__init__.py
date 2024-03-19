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
trigger.py

Base class to be used accross project
"""
import os
import typing
from ..info import mro


class Trigger:
    """
    Trigger

    Class to be (co)inherited in any class of the project.
    All actions will be logged.
    """

    def __init__(self, logger: typing.Callable = print):
        self.logger_callback = logger
        self.loglevel = "info"
        if os.environ.get("LOGLEVEL"):
            self._loglevel = os.environ.get("LOGLEVEL")

    @property
    def logger_callback(self):
        """Getter for logger callback"""
        return self._logger_callback

    @logger_callback.setter
    def logger_callback(self, value: typing.Callable):
        """Setter for logger callback"""
        self._logger_callback = value

    @property
    def loglevel(self):
        """Getter for loglevel"""
        return self._loglevel

    @loglevel.setter
    def loglevel(self, value):
        """Setter for loglevel"""
        if value in ("info", "warn", "debug"):
            self._loglevel = value
        else:
            raise ValueError(f"Invalid loglevel: {value}")

    def create_msg(self, msg):
        """
        Create the logged message with current
        class caller
        """
        caller = mro()
        return f"[{caller}]: {msg}"

    def info(self, msg):
        """
        Create the info message with the current
        class caller
        """
        if self.loglevel == "info":
            self.logger_callback(f"[INFO ] {self.create_msg(msg)}")

    def warn(self, msg):
        """
        Create the info message with the current
        class caller
        """
        if self.loglevel == "info":
            self.logger_callback(f"[WARN ] {self.create_msg(msg)}")

    def debug(self, msg):
        """
        Create the debug message with the current
        class caller
        """
        if self.loglevel == "debug":
            self.logger_callback(f"[DEBUG] {self.create_msg(msg)}")
