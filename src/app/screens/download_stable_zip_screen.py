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
download_stable_zip_screen.py
"""
import math
import time
from threading import Thread
from functools import partial
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.uix.label import Label
from src.app.screens.base_screen import BaseScreen
from src.utils.downloader.zip_downloader import ZipDownloader


class DownloadStableZipScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="download_stable_zip_screen", name="DownloadStableZipScreen", **kwargs
        )
        self.make_grid(wid="download_stable_zip_screen_grid", rows=2)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(Window.width, Window.height))

        self.downloader = None
        self.downloader_thread = None
        self.downloader_trigger = None
        self.version = None

        # progress label
        progress = Label(
            text="[size=40sp]Connecting...[/size]",
            markup=True,
            valign="center",
            halign="center",
        )
        progress.id = "download_progress"
        self.ids["download_stable_zip_screen_grid"].add_widget(progress)
        self.ids[progress.id] = WeakProxy(progress)

        # build label
        asset_label = Label(markup=True, valign="center", halign="center")
        asset_label.id = "asset_label"
        self.ids["download_stable_zip_screen_grid"].add_widget(asset_label)
        self.ids[asset_label.id] = WeakProxy(asset_label)

    def update(self, *args, **kwargs):
        """Update screen with version key"""
        if kwargs.get("key") == "version":
            self.version = kwargs.get("value")
            self.downloader = ZipDownloader(
                version=self.version,
                destdir=App.get_running_app().config.get("destdir", "assets"),
            )

            def on_progress(data: bytes):
                # calculate downloaded percentage
                len1 = self.downloader.downloaded_len
                len2 = self.downloader.content_len
                p = len1 / len2

                # Format bytes (one liner)
                # https://stackoverflow.com/questions/
                # 5194057/better-way-to-convert-file-sizes-in-python#answer-52684562
                down1 = f"{len1/(1<<20):,.2f}"
                down2 = f"{len2/(1<<20):,.2f}"

                # Put all in Label widget
                self.ids["download_progress"].text = "\n".join(
                    [
                        f"[size=100sp][b]{p * 100.00:.2f}%[/b][/size]",
                        f"[size=16sp]{down1} of {down2} MB[/size]",
                    ]
                )

                # When finish, change the label, wait some seconds
                # and then change screen
                if p == 1.00:
                    self.ids["asset_label"].text = "\n".join(
                        [
                            f"{self.downloader.destdir} downloaded",
                        ]
                    )
                    time.sleep(2)
                    self.downloader_trigger()

            self.downloader.on_write_to_buffer = on_progress

            self.ids["asset_label"].text = "\n".join(
                [
                    "Downloading",
                    f"[color=#00AABB][ref={self.downloader.url}]{self.downloader.url}[/ref][/color]",
                    "" f"to {self.downloader.destdir}",
                ]
            )

    def on_enter(self):
        """Event fired when the screen is displayed and the entering animation is complete"""
        self.downloader_thread = Thread(name=self.name, target=self.downloader.download)
        self.downloader_thread.start()

        # https://kivy.org/doc/stable/guide/events.html
        # wait until download thread finish, when finished
        # call this callback
        def callback(dt):
            screen = self.manager.get_screen("DownloadStableZipSha256Screen")
            fn = partial(screen.update, key="version", value=self.version)
            Clock.schedule_once(fn, 0)
            self.set_screen(name="DownloadStableZipSha256Screen", direction="left")

        self.downloader_trigger = Clock.create_trigger(callback)
