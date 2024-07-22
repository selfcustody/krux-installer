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
from kivy.logger import Logger
from ..info import mro


class Trigger:
    """
    Trigger

    Class to be (co)inherited in any class of the project.
    All actions will be logged.
    """

    def info(self, msg: str):
        """Logger with level 'info'"""
        Logger.info("%s: %s", mro(), msg)

    def debug(self, msg: str):
        """Logger with level 'debug'"""
        Logger.debug("%s: %s", mro(), msg)

    def warning(self, msg: str):
        """Logger with level 'warning'"""
        Logger.warning("%s: %s", mro(), msg)

    def error(self, msg: str):
        """Logger with level 'critical'"""
        Logger.error("%s: %s", mro(), msg)

    def critical(self, msg: str):
        """Logger with level 'critical'"""
        Logger.critical("%s: %s", mro(), msg)
