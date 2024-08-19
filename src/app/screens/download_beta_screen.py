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
import time
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from src.app.screens.base_download_screen import BaseDownloadScreen
from src.utils.downloader.beta_downloader import BetaDownloader


class DownloadBetaScreen(BaseDownloadScreen):
    """DownloadBetaScreen manage the download process of beta releases"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="download_beta_screen", name="DownloadBetaScreen", **kwargs
        )
        self.to_screen = "FlashScreen"
        self.firmware = None
        self.device = None

        # Define some staticmethods in dynamic way
        # (so they can be called in tests)
        def on_trigger(dt):
            time.sleep(2.1)
            screen = self.manager.get_screen(self.to_screen)
            baudrate = DownloadBetaScreen.get_baudrate()
            destdir = DownloadBetaScreen.get_destdir_assets()
            firmware = os.path.join(
                destdir, "krux_binaries", f"maixpy_{self.device}", self.firmware
            )
            partials = [
                partial(screen.update, name=self.name, key="baudrate", value=baudrate),
                partial(screen.update, name=self.name, key="firmware", value=firmware),
                partial(screen.update, name=self.name, key="flasher"),
            ]

            for fn in partials:
                Clock.schedule_once(fn, 0)

            self.set_screen(name=self.to_screen, direction="left")

        def on_progress(data: bytes):
            # calculate downloaded percentage
            if self.downloader is not None:
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

            else:
                self.redirect_error("Downloader isnt initialized")

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

        if name in ("ConfigKruxInstaller", "MainScreen", "DownloadBetaScreen"):
            self.debug(f"Updating {self.name} from {name}::{key}={value}")
        else:
            self.redirect_error(f"Invalid screen name: {name}")
            return

        if key == "locale":
            if value is not None:
                self.locale = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "canvas":
            # prepare background
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        elif key == "firmware":
            if value is None:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")
            elif value in ("kboot.kfpkg", "firmware.bin"):
                self.firmware = value
            else:
                self.redirect_error(f"Invalid firmware: {value}")

        elif key == "device":
            if value in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
                self.device = value
            else:
                self.redirect_error(f'Invalid device: "{value}"')

        elif key == "downloader":

            if self.downloader is None:
                destdir = DownloadBetaScreen.get_destdir_assets()
                destdir = os.path.join(
                    destdir, "krux_binaries", f"maixpy_{self.device}"
                )

                self.downloader = BetaDownloader(
                    device=self.device,
                    binary_type=self.firmware,
                    destdir=destdir,
                )

                downloading = self.translate("Downloading")
                to = self.translate("to")

                self.ids[f"{self.id}_info"].text = "".join(
                    [
                        f"[size={self.SIZE_MP}sp]",
                        f"[font={DownloadBetaScreen.get_font_name()}]",
                        downloading,
                        "[/font]",
                        "\n",
                        "[color=#00AABB]",
                        f"[ref={self.downloader.url}]{self.downloader.url}[/ref]",
                        "[/color]",
                        "\n",
                        f"[font={DownloadBetaScreen.get_font_name()}]",
                        to,
                        "[/font]",
                        "\n",
                        self.downloader.destdir,
                        "\n",
                        "[/size]",
                    ]
                )

            else:
                self.redirect_error("Downloader already initialized")

        elif key == "progress":
            # calculate percentage of download
            if value is not None and self.downloader is not None:
                lens = [value["downloaded_len"], value["content_len"]]
                percent = lens[0] / lens[1]

                # Format bytes (one liner) in MB
                # https://stackoverflow.com/questions/
                # 5194057/better-way-to-convert-file-sizes-in-python#answer-52684562
                downs = [f"{lens[0]/(1<<20):,.2f}", f"{lens[1]/(1<<20):,.2f}"]
                self.ids[f"{self.id}_progress"].text = "".join(
                    [
                        "[font=terminus]",
                        f"[size={self.SIZE_G}sp][b]{ percent * 100:,.2f} %[/b][/size]",
                        "\n",
                        f"[size={self.SIZE_MP}sp]{downs[0]} of {downs[1]} MB[/size]",
                        "[/font]",
                    ]
                )

                if percent == 1.0:
                    downloaded = self.translate("downloaded")
                    destdir = os.path.join(self.downloader.destdir, "kboot.kfpkg")
                    self.ids[f"{self.id}_info"].text = "".join(
                        [
                            f"[font={DownloadBetaScreen.get_font_name()}]",
                            f"[size={self.SIZE_MP}sp]",
                            destdir,
                            "\n",
                            downloaded,
                            "[/size]",
                            "[/font]",
                        ]
                    )

                    # When finish, change the label, wait some seconds
                    # and then change screen
                    self.trigger()

        else:
            self.redirect_error(f'Invalid key: "{key}"')
