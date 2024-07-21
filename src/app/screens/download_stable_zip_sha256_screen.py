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
download_stable_zip_sha256_screen.py
"""
import time
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from src.app.screens.base_screen import BaseScreen
from src.app.screens.base_download_screen import BaseDownloadScreen
from src.utils.downloader.sha256_downloader import Sha256Downloader


class DownloadStableZipSha256Screen(BaseDownloadScreen):
    """DownloadStableZipSha256Screen download the sha256sum file for official krux zip release"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="download_stable_zip_sha256_screen",
            name="DownloadStableZipSha256Screen",
            **kwargs,
        )
        self.to_screen = "DownloadStableZipSigScreen"

        # Define some staticmethods in dynamic way
        # (so they can be called in tests)
        def on_trigger(dt):
            time.sleep(2.1)
            screen = self.manager.get_screen(self.to_screen)
            fn = partial(
                screen.update, name=self.name, key="version", value=self.version
            )
            Clock.schedule_once(fn, 0)
            self.set_screen(name=self.to_screen, direction="left")

        def on_progress(data: bytes):
            # calculate downloaded percentage
            fn = partial(
                self.update,
                name=self.name,
                key="progress",
                value={
                    "downloaded_len": self.downloader.downloaded_len,
                    "content_len": self.downloader.content_len,
                },
            )
            Clock.schedule_once(fn, 0)

        self.debug(f"Bind {self.__class__}.on_trigger={on_trigger}")
        setattr(self.__class__, "on_trigger", on_trigger)

        self.debug(f"Bind {self.__class__}.on_progress={on_progress}")
        setattr(self.__class__, "on_progress", on_progress)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def update(self, *args, **kwargs):
        """Update screen with version key. Should be called before `on_enter`"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen name: {name}")

        if key == "locale":
            self.locale = value

        elif key == "canvas":
            # prepare background
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        elif key == "version":
            self.version = value
            self.downloader = Sha256Downloader(
                version=value,
                destdir=App.get_running_app().config.get("destdir", "assets"),
            )

            self.ids[f"{self.id}_info"].text = "\n".join(
                [
                    "Downloading",
                    f"[color=#00AABB][ref={self.downloader.url}]{self.downloader.url}[/ref][/color]",
                    ""
                    f"to {self.downloader.destdir}/krux-{self.version}.zip.sha256.txt",
                ]
            )

        elif key == "progress":
            # calculate percentage of download
            lens = [value["downloaded_len"], value["content_len"]]
            percent = lens[0] / lens[1]

            self.ids[f"{self.id}_progress"].text = "\n".join(
                [
                    f"[size=100sp][b]{ percent * 100:,.2f} %[/b][/size]",
                    "",
                    f"[size=16sp]{lens[0]} of {lens[1]} B[/size]",
                ]
            )

            if percent == 1.00:
                self.ids[f"{self.id}_info"].text = "\n".join(
                    [
                        f"{self.downloader.destdir}/krux-{self.version}.zip.sha256.txt downloaded",
                    ]
                )

                # When finish, change the label, wait some seconds
                # and then change screen
                self.trigger()

        else:
            raise ValueError(f'Invalid key: "{key}"')
