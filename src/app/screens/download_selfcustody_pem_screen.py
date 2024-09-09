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
download_selfcustody_pem_screen.py
"""
import os
import time
from typing import Any
from functools import partial
from kivy.clock import Clock
from src.app.screens.base_download_screen import BaseDownloadScreen
from src.utils.downloader.pem_downloader import PemDownloader


class DownloadSelfcustodyPemScreen(BaseDownloadScreen):
    """DownloadSelfcustodyPemScreen download the selfcustody's public key certificate"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="download_selfcustody_pem_screen",
            name="DownloadSelfcustodyPemScreen",
            **kwargs,
        )

        self.to_screen = "VerifyStableZipScreen"

        # Define some staticmethods in dynamic way
        # (so they can be called in tests)
        # pylint: disable=unused-argument
        def on_trigger(dt):
            time.sleep(2.1)
            self.set_screen(name=self.to_screen, direction="left")

        def on_progress(data: bytes):
            self.debug(f"Chunck length: {len(data)}")
            dl_len = getattr(self.downloader, "downloaded_len")
            ct_len = getattr(self.downloader, "content_len")
            # calculate downloaded percentage
            fn = partial(
                self.update,
                name=self.name,
                key="progress",
                value={"downloaded_len": dl_len, "content_len": ct_len},
            )
            Clock.schedule_once(fn, 0)

        setattr(DownloadSelfcustodyPemScreen, "on_trigger", on_trigger)
        setattr(DownloadSelfcustodyPemScreen, "on_progress", on_progress)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def on_update_pem(self):
        """Update public key certificate on GUI"""
        self.downloader = PemDownloader(
            destdir=DownloadSelfcustodyPemScreen.get_destdir_assets()
        )

        url = getattr(self.downloader, "url")
        destdir = getattr(self.downloader, "destdir")
        downloading = self.translate("Downloading")
        to = self.translate("to")
        filepath = os.path.join(destdir, "selfcustody.pem")

        self.ids[f"{self.id}_info"].text = "".join(
            [
                f"[size={self.SIZE_MP}sp]",
                downloading,
                "\n",
                f"[color=#00AABB][ref={url}]{url}[/ref][/color]",
                "\n",
                to,
                "\n",
                filepath,
                "[/size]",
            ]
        )

    def on_update_progress(self, value: Any):
        """Update the progress on GUI"""
        # calculate percentage of download
        lens = [value["downloaded_len"], value["content_len"]]

        percent = lens[0] / lens[1]

        # for some unknow reason (yet)
        # the screen show that downloaded
        # 130B of 128B, so limit it to 128
        percent = 1.0 if percent >= 1.0 else percent

        if lens[0] > lens[1]:
            lens[0] = lens[1]

        of = self.translate("of")
        self.ids[f"{self.id}_progress"].text = "".join(
            [
                f"[size={self.SIZE_G}sp][b]{percent * 100:,.2f} %[/b][/size]",
                "\n",
                f"[size={self.SIZE_MP}sp]",
                str(lens[0]),
                f" {of} ",
                str(lens[1]),
                " B",
                "[/size]",
            ]
        )

        if percent == 1.00:
            destdir = getattr(self.downloader, "destdir")
            downloaded = self.translate("downloaded")
            filepath = os.path.join(destdir, "selfcustody.pem")
            self.ids[f"{self.id}_info"].text = "".join(
                [
                    f"[size={self.SIZE_MP}sp]",
                    filepath,
                    "\n",
                    downloaded,
                    "[/size]",
                ]
            )

            # When finish, change the label, wait some seconds
            # and then change screen
            # trigger is defined in superclass
            callback_trigger = getattr(self, "trigger")
            callback_trigger()

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update screen with version key. Should be called before `on_enter`"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "public-key-certificate":
                on_update_pem = getattr(self, "on_update_pem")
                on_update_pem()

            if key == "progress":
                on_progress = getattr(self, "on_update_progress")
                on_progress(value)

        setattr(DownloadSelfcustodyPemScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "DownloadStableZipSigScreen",
                "DownloadSelfcustodyPemScreen",
            ),
            on_update=getattr(DownloadSelfcustodyPemScreen, "on_update"),
        )
