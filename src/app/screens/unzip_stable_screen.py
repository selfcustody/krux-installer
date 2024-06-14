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
verify_stable_zip_screen.py
"""
import time
from functools import partial
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.app import App
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from src.utils.constants import get_name, get_version
from src.app.screens.base_screen import BaseScreen
from src.utils.unzip.kboot_unzip import KbootUnzip
from src.utils.unzip.firmware_unzip import FirmwareUnzip


class UnzipStableScreen(BaseScreen):
    """VerifyStableZipScreen check for sha256sum and siganture"""

    def __init__(self, **kwargs):
        super().__init__(wid="unzip_stable_screen", name="UnzipStableScreen", **kwargs)
        self.make_grid(wid=f"{self.id}_grid", rows=2)
        # with self.canvas.before:
        #    Color(0, 0, 0, 1)
        #    Rectangle(size=(Window.width, Window.height))

    def update(self, *args, **kwargs):
        """Update widget from other screens"""

        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in ("ConfigKruxInstaller"):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            self.locale = value

    def on_pre_enter(self):
        """Before enter screen, configure some texts and widgets"""
        self.ids[f"{self.id}_grid"].clear_widgets()

        flash_msg = self.translate("Flash update with")
        airgap_msg = self.translate("Airgap update with")
        extract_msg = self.translate("Unziping")
        extracted_msg = self.translate("Unziped")

        assets_dir = App.get_running_app().config.get("destdir", "assets")
        main_screen = self.manager.get_screen("MainScreen")
        zip_file = f"{assets_dir}/krux-{main_screen.version}.zip"
        base_path = f"krux-{main_screen.version}/maixpy_{main_screen.device}"

        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            if instance.id == f"{self.id}_flash_button":
                file_path = f"{base_path}/kboot.kfpkg"

            if instance.id == f"{self.id}_airgap_button":
                file_path = f"{base_path}/firmware.bin"

            self.ids[instance.id].text = "\n".join(
                [extract_msg, f"[size=14sp][color=#efcc00]{file_path}[/color][/size]"]
            )
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            to_screen = None

            if instance.id == f"{self.id}_flash_button":
                file_path = f"{base_path}/kboot.kfpkg"
                unziper = KbootUnzip(
                    filename=zip_file, device=main_screen.device, output=assets_dir
                )
                to_screen = "FlashScreen"

            if instance.id == f"{self.id}_airgap_button":
                file_path = f"{base_path}/firmware.bin"
                unziper = FirmwareUnzip(
                    filename=zip_file, device=main_screen.device, output=assets_dir
                )
                to_screen = "AirgapScreen"

            screen = self.manager.get_screen(to_screen)
            fns = [
                partial(screen.update, key="firmware", value=file_path),
                partial(screen.update, key="device", value=main_screen.device),
            ]
            for fn in fns:
                Clock.schedule_once(fn, 0)

            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            unziper.load()

            self.ids[instance.id].text = "\n".join(
                [extracted_msg, f"[size=12sp][color=#efcc00]{file_path}[/color][/size]"]
            )

            time.sleep(4)
            self.set_screen(name=to_screen, direction="left")

        self.make_button(
            id=f"{self.id}_flash_button",
            root_widget=f"{self.id}_grid",
            text=f"\n".join(
                [
                    flash_msg,
                    f"[size=14sp][color=#efcc00]{assets_dir}/krux-{main_screen.version}/maixpy_{main_screen.device}/kboot.kfpkg[/color][/size]",
                ]
            ),
            markup=True,
            row=0,
            on_press=_press,
            on_release=_release,
        )

        self.make_button(
            id=f"{self.id}_airgap_button",
            root_widget=f"{self.id}_grid",
            text="\n".join(
                [
                    airgap_msg,
                    f"[size=14sp][color=#efcc00]{assets_dir}/krux-{main_screen.version}/maixpy_{main_screen.device}/firmware.bin[/color][/size]",
                ]
            ),
            markup=True,
            row=0,
            on_press=_press,
            on_release=_release,
        )
