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
download_stable_zip_sig_screen.py
"""
import os
import time
from functools import partial
from kivy.clock import Clock
from src.app.screens.base_download_screen import BaseDownloadScreen
from src.utils.downloader.sig_downloader import SigDownloader


class DownloadStableZipSigScreen(BaseDownloadScreen):
    """DownloadStableZipSigScreen download the sig file for official krux zip release"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="download_stable_zip_sig_screen",
            name="DownloadStableZipSigScreen",
            **kwargs,
        )
        self.to_screen = "DownloadSelfcustodyPemScreen"

        # Define some staticmethods in dynamic way
        # (so they can be called in tests)
        def on_trigger(dt):
            self.debug(f"latter call timed {dt}ms")
            time.sleep(2.1)
            screen = self.manager.get_screen(self.to_screen)
            fn = partial(screen.update, name=self.name, key="public-key-certificate")
            Clock.schedule_once(fn, 0)
            self.set_screen(name=self.to_screen, direction="left")

        def on_progress(data: bytes):
            # calculate downloaded percentage
            self.debug(f"Chunck size: {len(data)}")
            dl_len = getattr(self.downloader, "downloaded_len")
            ct_len = getattr(self.downloader, "content_len")
            fn = partial(
                self.update,
                name=self.name,
                key="progress",
                value={"downloaded_len": dl_len, "content_len": ct_len},
            )
            Clock.schedule_once(fn, 0)

        setattr(DownloadStableZipSigScreen, "on_trigger", on_trigger)
        setattr(DownloadStableZipSigScreen, "on_progress", on_progress)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update screen with version key. Should be called before `on_enter`"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            self.update_download_screen(key=key, value=value)

        setattr(DownloadStableZipSigScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "DownloadStableZipSha256Screen",
                "DownloadStableZipSigScreen",
            ),
            on_update=getattr(DownloadStableZipSigScreen, "on_update"),
        )

    def build_downloader(self, value: str):
        """Creates a Downloader for signature file given a firmware version"""
        self.version = value
        self.downloader = SigDownloader(
            version=self.version,
            destdir=DownloadStableZipSigScreen.get_destdir_assets(),
        )

        url = getattr(self.downloader, "url")
        destdir = getattr(self.downloader, "destdir")

        self.ids[f"{self.id}_info"].text = (
            DownloadStableZipSigScreen.make_download_info(
                download_msg=self.translate("Downloading"),
                from_url=url,
                to_msg=self.translate("to"),
                to_path=os.path.join(destdir, f"krux-{self.version}.zip.sig"),
            )
        )

    def on_download_progress(self, value: dict):
        """update GUI given a ration between what is downloaded and its total length"""
        # calculate percentage of download
        downloaded_len = value["downloaded_len"]
        content_len = value["content_len"]
        percent = downloaded_len / content_len

        self.ids[f"{self.id}_progress"].text = (
            DownloadStableZipSigScreen.make_progress_info(
                of_msg=self.translate("of"),
                percent=percent,
                downloaded_len=downloaded_len,
                content_len=content_len,
            )
        )

        # When finish, change the label
        # and then change screen
        if percent == 1.00:
            destdir = getattr(self.downloader, "destdir")
            downloaded = self.translate("downloaded")
            filepath = os.path.join(destdir, f"krux-{self.version}.zip.sig")
            self.ids[f"{self.id}_info"].text = "".join(
                [
                    filepath,
                    "\n",
                    downloaded,
                ]
            )

            # When finish, change the label, wait some seconds
            # and then change screen
            # trigger is defined in superclass
            callback_trigger = getattr(self, "trigger")
            callback_trigger()
