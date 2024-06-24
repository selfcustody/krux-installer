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
base_download_screen.py
"""
import typing
from functools import partial
from threading import Thread
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.clock import Clock, ClockEvent
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.uix.label import Label
from src.app.screens.base_screen import BaseScreen
from src.utils.downloader.asset_downloader import AssetDownloader


class BaseDownloadScreen(BaseScreen):
    """BaseDownloadScreen setup some initial variables for usable Downloader screens"""

    def __init__(self, wid: str, name: str, **kwargs):
        super().__init__(wid=wid, name=name, **kwargs)
        self.make_grid(wid=f"{self.id}_grid", rows=2)

        # since labels update to fast
        # maybe its better to increase
        # the default value of `Clock.max_iteration`
        Clock.max_iteration = 20

        self.downloader = None
        self.thread = None
        self.trigger = None
        self.version = None
        self.to_screen = None

        # prepare background
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(Window.width, Window.height))

        # progress label
        progress = Label(
            text="[size=40sp]Connecting...[/size]",
            markup=True,
            valign="center",
            halign="center",
        )

        # information label
        asset_label = Label(markup=True, valign="center", halign="center")

        # setup progress label
        progress.id = f"{self.id}_label_progress"
        self.ids[f"{self.id}_grid"].add_widget(progress)
        self.ids[progress.id] = WeakProxy(progress)

        # setup information label
        asset_label.id = f"{self.id}_label_info"
        self.ids[f"{self.id}_grid"].add_widget(asset_label)
        self.ids[asset_label.id] = WeakProxy(asset_label)

    @property
    def to_screen(self) -> str:
        self.debug(f"getter::to_screen={self._to_screen}")
        return self._to_screen

    @to_screen.setter
    def to_screen(self, value: str):
        self.debug(f"setter::to_screen={value}")
        self._to_screen = value

    @property
    def downloader(self) -> AssetDownloader:
        self.debug(f"getter::downloader={self._downloader}")
        return self._downloader

    @downloader.setter
    def downloader(self, value: AssetDownloader):
        self.debug(f"setter::downloader={value}")
        self._downloader = value

    @property
    def thread(self) -> Thread:
        self.debug(f"getter::thread={self._thread}")
        return self._thread

    @thread.setter
    def thread(self, value: typing.Callable):
        """
        Wait until download thread finish,
        when finished call this callback

        See https://kivy.org/doc/stable/guide/events.html
        """
        if not value is None:
            self._thread = Thread(name=self.name, target=value)
        else:
            self._thread = value

        self.debug(f"setter::thread={self._thread}->{value}")

    @property
    def trigger(self) -> ClockEvent:
        """Trigger is a `ClockEvent` that should be triggered after download is done"""
        self.debug(f"getter::trigger={self._thread}")
        return self._trigger

    @trigger.setter
    def trigger(self, value: typing.Callable):
        """Create a `ClockEvent` given a callback"""
        if not value is None:
            self._trigger = Clock.create_trigger(value)
        else:
            self._trigger = None
        self.debug(f"getter::trigger={self._thread}")

    def on_enter(self):
        """
        Event fired when the screen is displayed and the entering animation is complete.

        Every inherithed class should implement it own `on_trigger` and `on_progress`
        staticmethods. The method `on_progress` should call `self.trigger` ath the end:

        ```python
        Myclass(BaseDownloadScreen):

            def __init__(self, *args, **kwargs):
                super().__init__(wid="example_screen", name="ExampleScreen", **kwargs)

                def on_trigger(dt):
                    # do something

                def on_progress(data: bytes):
                    # do something
                    self.trigger()

                setattr(self.__class__, "on_trigger", on_trigger)
                setattr(self.__class__, "on_progress", on_progress)
        ```
        """
        if not self.downloader is None:
            self.trigger = getattr(self.__class__, "on_trigger")
            self.downloader.on_write_to_buffer = getattr(self.__class__, "on_progress")
            self.thread = self.downloader.download
            self.thread.start()
        else:
            raise ValueError("Downloader isnt configured. Use `update` method first")
