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
from threading import Thread
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.clock import Clock, ClockEvent
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.uix.label import Label
from src.utils.downloader.asset_downloader import AssetDownloader


class BaseDownloadScreen:
    """BaseDownloadScreen setup some initial variables for usable Downloader screens"""

    def __init__(self):
        self.downloader = None
        self.thread = None
        self.trigger = None
        self.version = None
        self.to_screen = None

    @property
    def downloader(self) -> AssetDownloader:
        self.debug(f"downloader::getter={self._downloader}")
        return self._downloader

    @downloader.setter
    def downloader(self, value: AssetDownloader):
        self.debug(f"downloader::setter={value}")
        self._downloader = value

    @property
    def thread(self) -> Thread:
        self.debug(f"thread::getter={self._thread}")
        return self._thread

    @thread.setter
    def thread(self, value: Thread):
        self.debug(f"thread::setter={value}")
        self._thread = value

    @property
    def trigger(self) -> ClockEvent:
        self.debug(f"trigger::getter={self._trigger}")
        return self._trigger

    @trigger.setter
    def trigger(self, value: ClockEvent):
        self.debug(f"trigger::setter={value}")
        self._trigger = value

    def setup(self, wid: str, to_screen: str):
        self.to_screen = to_screen

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
        progress.id = f"{wid}_label_progress"
        self.ids[f"{wid}_grid"].add_widget(progress)
        self.ids[progress.id] = WeakProxy(progress)

        # build label
        asset_label = Label(markup=True, valign="center", halign="center")
        asset_label.id = f"{wid}_label_info"
        self.ids[f"{wid}_grid"].add_widget(asset_label)
        self.ids[asset_label.id] = WeakProxy(asset_label)

    def build_thread(self, callback: typing.Callable):
        # https://kivy.org/doc/stable/guide/events.html
        # wait until download thread finish, when finished
        # call this callback
        self.trigger = Clock.create_trigger(callback)
        self.thread = Thread(name=self.name, target=self.downloader.download)
