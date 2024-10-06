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
import time
from functools import partial
from kivy.clock import Clock
from src.app.screens.base_screen import BaseScreen
from src.utils.unzip.kboot_unzip import KbootUnzip
from src.utils.unzip.firmware_unzip import FirmwareUnzip


class UnzipStableScreen(BaseScreen):
    """VerifyStableZipScreen check for sha256sum and siganture"""

    def __init__(self, **kwargs):
        super().__init__(wid="unzip_stable_screen", name="UnzipStableScreen", **kwargs)
        self.make_grid(wid=f"{self.id}_grid", rows=2)
        self.assets_dir = UnzipStableScreen.get_destdir_assets()
        self.device = None
        self.version = None

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update widget from other screens"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = str(kwargs.get("value"))

        def on_update():
            if key == "version":
                self.version = value

            if key == "device":
                self.device = value

            if key == "clear":
                self.debug(f"Clearing '{self.id}_grid'")
                self.ids[f"{self.id}_grid"].clear_widgets()

            if key == "flash-button":
                build = getattr(self, "build_extract_to_flash_button")
                build()

            if key == "airgap-button":
                build = getattr(self, "build_extract_to_airgap_button")
                build()

        setattr(UnzipStableScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "VerifyStableZipScreen",
                "UnzipStableScreen",
            ),
            on_update=getattr(UnzipStableScreen, "on_update"),
        )

    def build_extract_to_flash_button(self):
        """Builds an upper button for flash firmware"""
        self.debug("Building flash button")
        zip_file = os.path.join(self.assets_dir, f"krux-{self.version}.zip")
        base_path = os.path.join(f"krux-{self.version}", f"maixpy_{self.device}")
        rel_path = os.path.join(self.assets_dir, base_path)
        flash_msg = self.translate("Flash with")
        extract_msg = self.translate("Unziping")
        extracted_msg = self.translate("Unziped")

        def on_press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            file_path = os.path.join(rel_path, "kboot.kfpkg")
            self.ids[instance.id].text = "".join(
                [
                    extract_msg,
                    "\n",
                    "[color=#efcc00]",
                    file_path,
                    "[/color]",
                ]
            )
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            file_path = os.path.join(base_path, "kboot.kfpkg")
            full_path = os.path.join(self.assets_dir, file_path)
            baudrate = UnzipStableScreen.get_baudrate()

            unziper = KbootUnzip(
                filename=zip_file,
                device=getattr(self, "device"),
                output=getattr(self, "assets_dir"),
            )

            # load variables to FlashScreen before get in
            screen = self.manager.get_screen("FlashScreen")
            fns = [
                partial(screen.update, name=self.name, key="firmware", value=full_path),
                partial(screen.update, name=self.name, key="baudrate", value=baudrate),
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
                    extracted_msg,
                    "\n",
                    "[color=#efcc00]",
                    p,
                    "[/color]",
                ]
            )

            time.sleep(2.1)
            self.set_screen(name="FlashScreen", direction="left")

        p = os.path.join(rel_path, "kboot.kfpkg")
        self.make_button(
            row=0,
            wid=f"{self.id}_flash_button",
            root_widget=f"{self.id}_grid",
            text="".join(
                [
                    flash_msg,
                    "\n",
                    "[color=#efcc00]",
                    p,
                    "[/color]",
                ]
            ),
            font_factor=42,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def build_extract_to_airgap_button(self):
        """Build a lower button to airgap update"""
        self.debug("Building airgap button")
        zip_file = os.path.join(self.assets_dir, f"krux-{self.version}.zip")
        base_path = os.path.join(f"krux-{self.version}", f"maixpy_{self.device}")
        rel_path = os.path.join(self.assets_dir, base_path)
        airgap_msg = self.translate("Air-gapped update with")

        extract_msg = self.translate("Unziping")
        extracted_msg = self.translate("Unziped")

        def on_press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            file_path = os.path.join(rel_path, "firmware.bin")
            self.ids[instance.id].text = "".join(
                [extract_msg, "\n", "[color=#efcc00]", file_path, "[/color]"]
            )
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            bin_path = os.path.join(base_path, "firmware.bin")
            bin_full_path = os.path.join(self.assets_dir, bin_path)

            sig_path = os.path.join(base_path, "firmware.bin.sig")
            sig_full_path = os.path.join(self.assets_dir, sig_path)

            unziper = FirmwareUnzip(
                filename=zip_file, device=self.device, output=self.assets_dir
            )

            # load variables to FlashScreen before get in
            screen = self.manager.get_screen("AirgapUpdateScreen")
            fns = [
                partial(
                    screen.update, name=self.name, key="binary", value=bin_full_path
                ),
                partial(
                    screen.update, name=self.name, key="signature", value=sig_full_path
                ),
            ]

            for fn in fns:
                Clock.schedule_once(fn, 0)

            # start the unzip process
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            unziper.load()

            # once unziped, give some messages
            self.ids[instance.id].text = "".join(
                [extracted_msg, "\n", "[color=#efcc00]", bin_full_path, "[/color]"]
            )

            time.sleep(2.1)
            self.set_screen(name="WarningBeforeAirgapUpdateScreen", direction="left")

        p = os.path.join(rel_path, "firmware.bin")
        self.make_button(
            row=1,
            wid=f"{self.id}_airgap_button",
            root_widget=f"{self.id}_grid",
            text="".join([airgap_msg, "\n", "[color=#efcc00]", p, "[/color]"]),
            font_factor=42,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )
