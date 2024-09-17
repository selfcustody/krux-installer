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
about_screen.py
"""
from typing import Any
from functools import partial
from kivy.clock import Clock
from src.app.screens.base_screen import BaseScreen


class WarningAlreadyDownloadedScreen(BaseScreen):
    """WarningAlreadyDownloadedScreen warns user about an asset that is already downloaded"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="warning_already_downloaded_screen",
            name="WarningAlreadyDownloadedScreen",
            **kwargs,
        )

        self.make_grid(wid=f"{self.id}_grid", rows=2, resize_canvas=True)

        self.make_image(
            wid=f"{self.id}_loader",
            source=self.warn_img,
            root_widget=f"{self.id}_grid",
        )

        def on_ref_press(*args):
            if args[1] == "DownloadStableZipScreen":
                main_screen = self.manager.get_screen("MainScreen")
                download_screen = self.manager.get_screen("DownloadStableZipScreen")
                fn = partial(
                    download_screen.update,
                    name=self.name,
                    key="version",
                    value=main_screen.version,
                )
                Clock.schedule_once(fn, 0)
                self.set_screen(name="DownloadStableZipScreen", direction="left")

            if args[1] == "VerifyStableZipScreen":
                self.set_screen(name="VerifyStableZipScreen", direction="left")

        self.make_button(
            row=0,
            wid=f"{self.id}_label",
            text="",
            halign=None,
            font_factor=32,
            root_widget=f"{self.id}_grid",
            on_press=None,
            on_release=None,
            on_ref_press=on_ref_press,
        )

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def on_warning(self, key: str, value: Any):
        """Update a warning message on GUI"""
        if key == "version":
            warning_msg = self.translate("Assets already downloaded")
            # ask_proceed = self.translate(
            #    "Do you want to proceed with the same file or do you want to download it again?"
            # )
            download_msg = self.translate("Download again")
            proceed_msg = self.translate("Proceed with current file")

            self.ids[f"{self.id}_label"].text = "".join(
                [
                    f"[color=#efcc00][b]{warning_msg}[/b][/color]",
                    "\n",
                    f"* krux-{value}.zip",
                    "\n",
                    f"* krux-{value}.zip.sha256.txt",
                    "\n",
                    f"* krux-{value}.zip.sig",
                    "\n",
                    "* selfcustody.pem",
                    "\n",
                    "\n",
                    "[color=#00ff00]",
                    "[ref=DownloadStableZipScreen]",
                    f"[u]{download_msg}[/u]",
                    "[/ref]",
                    "[/color]",
                    "        ",
                    "[color=#efcc00]",
                    "[ref=VerifyStableZipScreen]",
                    f"[u]{proceed_msg}[/u]",
                    "[/ref]",
                    "[/color]",
                ]
            )

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            self.on_warning(key, value)

        setattr(WarningAlreadyDownloadedScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "MainScreen",
                "WarningAlreadyDownloadedScreen",
            ),
            on_update=getattr(WarningAlreadyDownloadedScreen, "on_update"),
        )
