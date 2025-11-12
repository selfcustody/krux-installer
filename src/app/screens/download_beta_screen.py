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
from kivy.clock import Clock
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

        self.download_msg = self.translate("Downloading")
        self.to_message = self.translate("to")
        self.of_message = self.translate("of")

        # Define some staticmethods in dynamic way
        # (so they can be called in tests)
        # pylint: disable=unused-argument
        def on_trigger(dt):
            time.sleep(2.1)
            screen = self.manager.get_screen(self.to_screen)
            baudrate = DownloadBetaScreen.get_baudrate()
            destdir = DownloadBetaScreen.get_destdir_assets()
            _device = getattr(self, "device")
            maixpy = f"maixpy_{_device}"
            _firmware = getattr(self, "firmware")
            firmware = os.path.join(destdir, "krux_binaries", f"{maixpy}", _firmware)
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
            dl_len = getattr(self.downloader, "downloaded_len")
            ct_len = getattr(self.downloader, "content_len")
            fn = partial(
                self.update,
                name=self.name,
                key="progress",
                value={"downloaded_len": dl_len, "content_len": ct_len},
            )
            Clock.schedule_once(fn, 0)

        self.debug(f"Bind {self.__class__}.on_trigger={on_trigger}")
        setattr(self.__class__, "on_trigger", on_trigger)

        self.debug(f"Bind {self.__class__}.on_progress={on_progress}")
        setattr(self.__class__, "on_progress", on_progress)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update screen with version key. Should be called before `on_enter`"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "locale":
                self.download_msg = self.translate("Downloading")
                self.to_message = self.translate("to")
                self.of_message = self.translate("of")

            if key == "firmware":
                if value in ("kboot.kfpkg", "firmware.bin"):
                    self.firmware = value
                else:
                    error = RuntimeError(f"Invalid value for key '{key}': {value}")
                    self.error(str(error))
                    self.redirect_exception(exception=error)

            if key == "device":
                if value in (
                    "m5stickv",
                    "amigo",
                    "dock",
                    "bit",
                    "yahboom",
                    "cube",
                    "wonder_mv",
                    "tzt",
                    "embed_fire",
                ):
                    self.device = value
                else:
                    error = RuntimeError(f"Invalid value for key '{key}': {value}")
                    self.error(str(error))
                    self.redirect_exception(exception=error)

            if key == "downloader":
                self.build_downloader()

            if key == "progress":
                self.on_download_progress(value)

        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("ConfigKruxInstaller", "MainScreen", "DownloadBetaScreen"),
            on_update=on_update,
        )

    def build_downloader(self):
        """Build the downloader for beta firmware before the download itself"""
        destdir = DownloadBetaScreen.get_destdir_assets()
        destdir = os.path.join(destdir, "krux_binaries", f"maixpy_{self.device}")

        self.downloader = BetaDownloader(
            device=self.device,
            binary_type=self.firmware,
            destdir=destdir,
        )

        self.ids[f"{self.id}_info"].text = "".join(
            [
                self.download_msg,
                "\n",
                "[color=#00AABB]",
                f"[ref={self.downloader.url}]{self.downloader.url}[/ref]",
                "[/color]",
                "\n",
                self.to_message,
                "\n",
                self.downloader.destdir,
                "\n",
            ]
        )

    def on_download_progress(self, value):
        """
        In each iteration of downloaded chunks, update the GUI with a ratio between
        it's downloaded length and content length
        """
        # trigger is defined in superclass

        callback_trigger = getattr(self, "trigger")
        lens = [value["downloaded_len"], value["content_len"]]
        percent = lens[0] / lens[1]

        # Format bytes (one liner) in MB
        # https://stackoverflow.com/questions/
        # 5194057/better-way-to-convert-file-sizes-in-python#answer-52684562
        downs = [f"{lens[0]/(1<<20):,.2f}", f"{lens[1]/(1<<20):,.2f}"]
        self.ids[f"{self.id}_progress"].text = "".join(
            [
                f"[b]{ percent * 100:,.2f} %[/b]",
                "\n",
                f"{downs[0]} {self.of_message} {downs[1]} MB",
            ]
        )

        if percent == 1.0:
            downloaded = self.translate("downloaded")
            destdir = os.path.join(self.downloader.destdir, "kboot.kfpkg")
            self.ids[f"{self.id}_info"].text = "".join(
                [
                    destdir,
                    "\n",
                    downloaded,
                ]
            )

            # When finish, change the label, wait some seconds
            # and then change screen
            callback_trigger()
