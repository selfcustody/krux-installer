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
base_flash__screen.py
"""
import os
import typing
from threading import Thread
from kivy.clock import Clock, ClockEvent
from src.app.screens.base_screen import BaseScreen


class BaseFlashScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, wid: str, name: str, **kwargs):
        super().__init__(wid=wid, name=name, **kwargs)
        self.make_grid(wid=f"{self.id}_grid", rows=2, resize_canvas=True)
        self._firmware = None
        self._baudrate = None
        self._thread = None
        self._output = []
        self._progress = None
        self._done = None
        self._is_done = False

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
    def thread(self, value: Thread):
        """
        Wait until download thread finish,
        when finished call this callback

        See https://kivy.org/doc/stable/guide/events.html
        """
        self.debug(f"setter::thread={self._thread}->{value}")
        self._thread = value

    @property
    def done(self) -> ClockEvent:
        """Trigger is a `ClockEvent` that should be triggered after download is done"""
        self.debug(f"getter::done={self._done}")
        return self._done

    @done.setter
    def done(self, value: typing.Callable):
        """Create a `ClockEvent` given a callback"""
        self.debug(f"getter::trigger={self._done}")
        self._done = Clock.create_trigger(value)

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
    def is_done(self) -> bool:
        """Getter for is_done"""
        self.debug(f"getter::is_done={self._is_done}")
        return self._is_done

    @is_done.setter
    def is_done(self, value: bool):
        """Setter for info"""
        self.debug(f"setter::is_done={value}")
        self._is_done = value

    def build_on_done(self):
        """
        Build a streaming IO static method using
        some instance variables when flash procedure is done

        (useful for to be used in tests)
        """

        # pylint: disable=unused-argument
        def on_done(dt):
            self.is_done = True
            del self.output[4:]
            self.ids[f"{self.id}_loader"].source = self.done_img
            self.ids[f"{self.id}_loader"].reload()
            done = self.translate("DONE")
            back = self.translate("Back")
            _quit = self.translate("Quit")

            self.ids[f"{self.id}_progress"].text = "".join(
                [
                    f"[b]{done}![/b]",
                    "\n",
                    "[color=#00FF00]",
                    f"[ref=Back][u]{back}[/u][/ref]",
                    "[/color]",
                    "        ",
                    "[color=#EFCC00]",
                    f"[ref=Quit][u]{_quit}[/u][/ref]",
                    "[/color]",
                ]
            )

        setattr(self.__class__, "on_done", on_done)

    @staticmethod
    def parse_general_output(text: str) -> str:
        """Parses KTool.print_callback output to make it more readable on GUI"""
        text = text.replace(
            "\x1b[32m\x1b[1m[INFO]\x1b[0m", "[color=#00ff00]INFO[/color]"
        )
        text = text.replace("\x1b[33mISP loaded", "[color=#efcc00]ISP loaded[/color]")
        text = text.replace(
            "\x1b[33mInitialize K210 SPI Flash",
            "[color=#efcc00]Initialize K210 SPI Flash[/color]",
        )
        text = text.replace("Flash ID: \x1b[33m", "Flash ID: [color=#efcc00]")
        text = text.replace(
            "\x1b[0m, unique ID: \x1b[33m", "[/color], unique ID: [color=#efcc00]"
        )
        text = text.replace("\x1b[0m, size: \x1b[33m", "[/color], size: ")
        text = text.replace("\x1b[0m MB", "[/color] MB")
        text = text.replace("\x1b[0m", "")
        text = text.replace("\x1b[33m", "")
        return text
