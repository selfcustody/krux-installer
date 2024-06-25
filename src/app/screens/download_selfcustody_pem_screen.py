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
import time
from kivy.app import App
from kivy.clock import Clock
from src.app.screens.base_screen import BaseScreen
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
        def on_trigger(dt):
            self.set_screen(name=self.to_screen, direction="left")

        def on_progress(data: bytes):
            len1 = self.downloader.downloaded_len
            len2 = self.downloader.content_len
            p = len1 / len2
            p = p if p <= 1.00 else 1.00
            self.ids[f"{self.id}_label_progress"].text = "\n".join(
                [
                    f"[size=100sp][b]{p * 100.00:.2f}%[/b][/size]",
                    f"[size=16sp]{len1} of {len2} B[/size]",
                ]
            )

            # When finish, change the label, wait some seconds
            # and then change screen
            if p == 1.00:
                self.ids[f"{self.id}_label_info"].text = "\n".join(
                    [
                        f"{self.downloader.destdir}/selfcustody.pem downloaded",
                    ]
                )
                time.sleep(2.1)  # 2.1 remember 21000000
                self.trigger()

        self.debug(f"Bind {self.__class__}.on_trigger={on_trigger}")
        setattr(self.__class__, "on_trigger", on_trigger)

        self.debug(f"Bind {self.__class__}.on_progress={on_progress}")
        setattr(self.__class__, "on_progress", on_progress)

    def update(self, *args, **kwargs):
        """Update screen with version key. Should be called before `on_enter`"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen name: {name}")

        if key == "locale":
            self.locale = value

        elif key == "public-key-certificate":
            self.downloader = PemDownloader(
                destdir=App.get_running_app().config.get("destdir", "assets"),
            )

            self.ids[f"{self.id}_label_info"].text = "\n".join(
                [
                    "Downloading",
                    f"[color=#00AABB][ref={self.downloader.url}]{self.downloader.url}[/ref][/color]",
                    "" f"to {self.downloader.destdir}/selfcustody.pem",
                ]
            )

        else:
            raise ValueError(f'Invalid key: "{key}"')
