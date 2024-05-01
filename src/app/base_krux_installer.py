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
krux_installer.py
"""
import os
import typing
import tempfile
from kivy.logger import Logger, LOG_LEVELS
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from ..utils.trigger import Trigger

DEFAULT_DESTDIR = tempfile.mkdtemp()
DEFAULT_BAUDRATE = 1500000
DEFAULT_LOCALE = "en-US"

if "LOGLEVEL" in os.environ:
    Logger.setLevel(LOG_LEVELS[os.environ["LOGLEVEL"]])
else:
    Logger.setLevel(LOG_LEVELS["info"])


class BaseKruxInstaller(App, Trigger):
    """BaseKruxInstller is the base for Appliction"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screens = []
        self.screen_manager = ScreenManager()

    @property
    def screens(self) -> typing.List[Screen]:
        """Getter of :class:`kivy.uix.screenmanager.Screen`"""
        self.debug(f"screens::setter={self._screens}")
        return self._screens

    @screens.setter
    def screens(self, value: typing.List[Screen]):
        """Setter of :class:`kivy.uix.screenmanager.Screen`"""
        self.debug(f"screens::getter={value}")
        self._screens = value

    @property
    def screen_manager(self) -> ScreenManager:
        """Getter of :class:`kivy.uix.screenmanager.ScreenManager`"""
        self.debug(f"screen_manager::setter={self._screen_manager}")
        return self._screen_manager

    @screen_manager.setter
    def screen_manager(self, value: typing.List[Screen]):
        """Setter of :class:`kivy.uix.screenmanager.ScreenManager`"""
        self.debug(f"screen_manager::getter={value}")
        self._screen_manager = value
