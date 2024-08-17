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
import os
import sys
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

        self.assets_dir = UnzipStableScreen.get_destdir_assets()
        self.device = None
        self.version = None

    def update(self, *args, **kwargs):
        """Update widget from other screens"""

        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in (
            "ConfigKruxInstaller",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            if value is not None:
                self.locale = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "version":
            if value is not None:
                self.version = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "device":
            if value is not None:
                self.device = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "clear":
            self.debug(f"Clearing '{self.id}_grid'")
            self.ids[f"{self.id}_grid"].clear_widgets()

        elif key == "flash-button":
            self.build_extract_to_flash_button()

        elif key == "airgap-button":
            self.build_extract_to_airgap_button()

        else:
            self.redirect_error(f'Invalid key: "{key}"')

    def build_extract_to_flash_button(self):
        self.debug("Building flash button")
        zip_file = os.path.join(self.assets_dir, f"krux-{self.version}.zip")
        base_path = os.path.join(f"krux-{self.version}", f"maixpy_{self.device}")
        rel_path = os.path.join(self.assets_dir, base_path)
        flash_msg = self.translate("Flash with")
        extract_msg = self.translate("Unziping")
        extracted_msg = self.translate("Unziped")
        size = [self.SIZE_MM, self.SIZE_MP]

        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            file_path = os.path.join(rel_path, "kboot.kfpkg")
            self.ids[instance.id].text = "".join(
                [
                    f"[font={UnzipStableScreen.get_font_name()}]",
                    f"[size={size[0]}sp]",
                    extract_msg,
                    "[/size]",
                    "\n",
                    f"[size={size[1]}sp]",
                    "[color=#efcc00]",
                    file_path,
                    "[/color]",
                    "[/size]",
                    "[/font]",
                ]
            )
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            if self.device is not None:
                file_path = os.path.join(base_path, "kboot.kfpkg")
                full_path = os.path.join(self.assets_dir, file_path)
                baudrate = UnzipStableScreen.get_baudrate()

                unziper = KbootUnzip(
                    filename=zip_file, device=self.device, output=self.assets_dir
                )

                # load variables to FlashScreen before get in
                screen = self.manager.get_screen("FlashScreen")
                fns = [
                    partial(
                        screen.update, name=self.name, key="firmware", value=full_path
                    ),
                    partial(
                        screen.update, name=self.name, key="baudrate", value=baudrate
                    ),
                    partial(screen.update, name=self.name, key="flasher"),
                ]

                for fn in fns:
                    Clock.schedule_once(fn, 0)

                # start the unzip process
                self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
                unziper.load()

                # once unziped, give some messages
                p = os.path.join(rel_path, "kboot.kfpkg")
                self.ids[instance.id].text = "".join(
                    [
                        f"[font={UnzipStableScreen.get_font_name()}]",
                        f"[size={size[0]}sp]",
                        extracted_msg,
                        "[/size]",
                        "\n",
                        f"[size={size[1]}sp]",
                        "[color=#efcc00]",
                        p,
                        "[/color]",
                        "[/size]",
                        "[/font]",
                    ]
                )

            time.sleep(2.1)
            self.set_screen(name="FlashScreen", direction="left")

        setattr(UnzipStableScreen, f"on_press_{self.id}_flash_button", _press)
        setattr(UnzipStableScreen, f"on_release_{self.id}_flash_button", _release)

        p = os.path.join(rel_path, "kboot.kfpkg")
        self.make_button(
            id=f"{self.id}_flash_button",
            root_widget=f"{self.id}_grid",
            text="".join(
                [
                    f"[font={UnzipStableScreen.get_font_name()}]",
                    f"[size={size[0]}sp]",
                    flash_msg,
                    "[/size]",
                    "\n",
                    f"[size={size[1]}sp]",
                    "[color=#efcc00]",
                    p,
                    "[/color]",
                    "[/size]",
                    "[/font]",
                ]
            ),
            markup=True,
            row=0,
            on_press=getattr(UnzipStableScreen, f"on_press_{self.id}_flash_button"),
            on_release=getattr(UnzipStableScreen, f"on_release_{self.id}_flash_button"),
        )

    def build_extract_to_airgap_button(self):
        self.debug("Building airgap button")
        zip_file = f"{self.assets_dir}/krux-{self.version}.zip"
        base_path = f"krux-{self.version}/maixpy_{self.device}"
        rel_path = f"{self.assets_dir}/{base_path}"
        airgap_msg = self.translate("Air-gapped update with")
        extract_msg = self.translate("Unziping")
        extracted_msg = self.translate("Unziped")

        size = [self.SIZE_MM, self.SIZE_MP]

        activated = False

        def _press(instance):
            if activated:
                self.debug(f"Calling Button::{instance.id}::on_press")
                file_path = os.path.join(rel_path, "firmware.bin")
                self.ids[instance.id].text = "".join(
                    [
                        f"[font={UnzipStableScreen.get_font_name()}]",
                        f"[size={size[0]}sp]",
                        extract_msg,
                        "[/size]",
                        "\n",
                        f"[size={size[1]}sp]",
                        "[color=#efcc00]",
                        file_path,
                        "[/color]",
                        "[/size]",
                        "[/font]",
                    ]
                )
                self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _release(instance):
            if activated:
                self.debug(f"Calling Button::{instance.id}::on_release")
                if self.device is not None:
                    file_path = f"{base_path}/firmware.bin"
                    unziper = FirmwareUnzip(
                        filename=zip_file, device=self.device, output=self.assets_dir
                    )

                    screen = self.manager.get_screen("AirgapScreen")
                    fns = [
                        partial(screen.update, key="firmware", value=file_path),
                        partial(screen.update, key="device", value=self.device),
                    ]
                    for fn in fns:
                        Clock.schedule_once(fn, 0)

                    self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
                    unziper.load()

                    p = os.path.join(rel_path, "firmware.bin")
                    self.ids[instance.id].text = "".join(
                        [
                            f"[font={UnzipStableScreen.get_font_name()}]",
                            f"[size={size[0]}sp]",
                            extracted_msg,
                            "[/size]",
                            "\n",
                            f"[size={size[1]}sp]",
                            "[color=#efcc00]",
                            p,
                            "[/color]",
                            "[/size]",
                            "[/font]",
                        ]
                    )

                    time.sleep(2.1)
                    self.set_screen(name="AirgapScreen", direction="left")

        setattr(UnzipStableScreen, f"on_press_{self.id}_airgap_button", _press)
        setattr(UnzipStableScreen, f"on_release_{self.id}_airgap_button", _release)

        p = os.path.join(rel_path, "firmware.bin")
        self.make_button(
            id=f"{self.id}_airgap_button",
            root_widget=f"{self.id}_grid",
            text="".join(
                [
                    f"[font={UnzipStableScreen.get_font_name()}]",
                    f"[size={size[0]}sp]",
                    "[color=#333333]",
                    airgap_msg,
                    "[/color]",
                    "[/size]",
                    "\n",
                    f"[size={size[1]}sp]",
                    "[color=#333333]",
                    p,
                    "[/color]",
                    "[/size]",
                    "[/font]",
                ]
            ),
            markup=True,
            row=0,
            on_press=getattr(UnzipStableScreen, f"on_press_{self.id}_airgap_button"),
            on_release=getattr(
                UnzipStableScreen, f"on_release_{self.id}_airgap_button"
            ),
        )
