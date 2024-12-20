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
import shutil
from functools import partial
from kivy.clock import Clock
from src.utils.verifyer.sha256_verifyer import Sha256Verifyer
from src.app.screens.base_screen import BaseScreen


class AirgapUpdateScreen(BaseScreen):
    """AirgapUpdateScreen is where user select a folder (generally a SDCard) to update device"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="airgap_update_screen", name="AirgapUpdateScreen", **kwargs
        )

        self._firmware_bin = ""
        self._firmware_sig = ""

    def build_drive_button(self, row: int, drive: str):
        """dynamically create a callback for copy process"""

        def on_press(instance):
            self.debug(f"Calling {instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        setattr(AirgapUpdateScreen, f"on_press_{self.id}_button_{row}", on_press)

        def on_release(instance):
            new_firmware_bin = os.path.normpath(os.path.join(drive, "firmware.bin"))
            new_firmware_sig = os.path.normpath(os.path.join(drive, "firmware.bin.sig"))
            shutil.copyfile(self.firmware_bin, new_firmware_bin)
            shutil.copyfile(self.firmware_sig, new_firmware_sig)

            # After copy, make sha256 hash to show
            sha256 = Sha256Verifyer(filename=new_firmware_bin)
            sha256.load()

            # Now update the next screen
            warn_screen = self.manager.get_screen("WarningAfterAirgapUpdateScreen")

            fns = [
                partial(
                    warn_screen.update,
                    name=self.name,
                    key="sdcard",
                    value=drive,
                ),
                partial(
                    warn_screen.update,
                    name=self.name,
                    key="hash",
                    value=sha256.data.split(" ", maxsplit=1)[0],
                ),
                partial(warn_screen.update, name=self.name, key="label"),
            ]

            for fn in fns:
                Clock.schedule_once(fn, 0)

            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            self.set_screen(name="WarningAfterAirgapUpdateScreen", direction="left")

        setattr(AirgapUpdateScreen, f"on_release_{self.id}_button_{row}", on_release)

        select = self.translate("Select")
        to_copy = self.translate("to copy firmware")

        # Now build the button
        self.make_button(
            root_widget=f"{self.id}_grid",
            wid=f"{self.id}_button_{row}",
            text="".join(
                [select, "\n", f"[color=#efcc00]{drive}[/color]", "\n", to_copy]
            ),
            row=row,
            halign="center",
            font_factor=36,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    # pylint: disable=unused-argument
    def on_leave(self, *args):
        self.info("Clearing widgets")
        self.clear_grid(wid=f"{self.id}_grid")
        del self.ids[f"{self.id}_grid"]

    @property
    def firmware_bin(self) -> str:
        """Getter for the full path of firmware.bin"""
        self.debug(f"{self.id}::firmware_bin::getter={self._firmware_bin}")
        return self._firmware_bin

    @firmware_bin.setter
    def firmware_bin(self, value: str):
        """Setter for the full path of firmware.bin"""
        self.debug(f"{self.id}::firmware_bin::setter={self._firmware_bin}")
        self._firmware_bin = value

    @property
    def firmware_sig(self) -> str:
        """Getter for the full path of firmware.bin.sig"""
        self.debug(f"{self.id}::firmware_sig::getter={self._firmware_sig}")
        return self._firmware_sig

    @firmware_sig.setter
    def firmware_sig(self, value: str):
        """Setter for the full path of firmware.bin.sig"""
        self.debug(f"{self.id}::firmware_sig::setter={self._firmware_sig}")
        self._firmware_sig = value

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update screen with firmware.bin and firmware.bin.sig"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "drives":
                self.make_grid(wid=f"{self.id}_grid", rows=len(value))
                for i, drive in enumerate(value):
                    self.build_drive_button(row=i, drive=drive)

            if key == "binary":
                self.firmware_bin = value

            if key == "signature":
                self.firmware_sig = value

        setattr(AirgapUpdateScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "UnzipStableScreen",
                "WarningBeforeAirgapUpdateScreen",
                "AirgapUpdateScreen",
            ),
            on_update=getattr(AirgapUpdateScreen, "on_update"),
        )
