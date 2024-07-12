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
main_screen.py
"""
import os
import math
import typing
from pathlib import Path
from functools import partial
from threading import Thread
from kivy.clock import Clock, ClockEvent
from src.utils.flasher import Flasher
from src.app.screens.base_screen import BaseScreen


class BaseFlashScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, wid: str, name: str, **kwargs):
        super().__init__(wid=wid, name=name, **kwargs)
        self.make_grid(wid=f"{self.id}_grid", rows=2)
        root_assets_path = Path(__file__).parent.parent.parent.parent
        self._warn_img = os.path.join(root_assets_path, "assets", "warning.png")
        self._done_img = os.path.join(root_assets_path, "assets", "done.png")
        self._firmware = None
        self._baudrate = None
        self._thread = None
        self._trigger = None
        self._output = None
        self._progress = None
        self._is_done = False

    @property
    def warn_img(self) -> str:
        """Getter for warn_img"""
        self.debug(f"getter::firmware={self._warn_img}")
        return self._warn_img

    @property
    def done_img(self) -> str:
        """Getter for done_img"""
        self.debug(f"getter::firmware={self._done_img}")
        return self._done_img

    @property
    def firmware(self) -> str:
        """Getter for firmware"""
        self.debug(f"getter::firmware={self._firmware}")
        return self._firmware

    @firmware.setter
    def firmware(self, value: str):
        """Setter for firmware"""
        if os.path.exists(value):
            self.debug(f"setter::firmware={value}")
            self._firmware = value
        else:
            raise ValueError(f"Firmware not exist: {value}")

    @property
    def baudrate(self) -> str:
        """Getter for baudrate"""
        self.debug(f"getter::baudrate={self._baudrate}")
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value: str):
        """Setter for baudrate"""
        self.debug(f"setter::baudrate={value}")
        self._baudrate = value

    @property
    def thread(self) -> Thread:
        """Getter for thread"""
        self.debug(f"getter::thread={self._thread}")
        return self._thread

    @thread.setter
    def thread(self, value: typing.Callable):
        """
        Wait until download thread finish,
        when finished call this callback

        See https://kivy.org/doc/stable/guide/events.html
        """
        self.debug(f"setter::thread={self._thread}->{value}")
        self._thread = Thread(name=self.name, target=value)

    @property
    def trigger(self) -> ClockEvent:
        """Trigger is a `ClockEvent` that should be triggered after download is done"""
        self.debug(f"getter::trigger={self._thread}")
        return self._trigger

    @trigger.setter
    def trigger(self, value: typing.Callable):
        """Create a `ClockEvent` given a callback"""
        self.debug(f"getter::trigger={self._trigger}")
        self._trigger = Clock.create_trigger(value)

    @property
    def output(self) -> typing.List[str]:
        """Getter for output"""
        self.debug(f"getter::output={self._output}")
        return self._output

    @output.setter
    def output(self, value: typing.List[str]):
        """Setter for info"""
        self.debug(f"setter::output={value}")
        self._output = value

    @property
    def progress(self) -> str:
        """Getter for progress"""
        self.debug(f"getter::progress={self._progress}")
        return self._progress

    @progress.setter
    def progress(self, value: str):
        """Setter for info"""
        self.debug(f"setter::progress={value}")
        self._progress = value

    @property
    def is_done(self) -> bool:
        """Getter for done"""
        self.debug(f"getter::done={self._is_done}")
        return self._is_done

    @is_done.setter
    def is_done(self, value: bool):
        """Setter for done"""
        self.debug(f"setter::done={value}")
        self._is_done = value
