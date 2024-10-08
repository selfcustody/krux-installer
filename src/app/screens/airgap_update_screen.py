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

        def on_load(path):
            new_firmware_bin = os.path.join(path, "firmware.bin")
            self.info(f"Copying file {self.firmware_bin} to {new_firmware_bin}")
            shutil.copyfile(self.firmware_bin, new_firmware_bin)

            new_firmware_sig = os.path.join(path, "firmware.bin.sig")
            self.info(f"Copying file {self.firmware_sig} to {new_firmware_sig}")
            shutil.copyfile(self.firmware_sig, new_firmware_sig)

            sha256 = Sha256Verifyer(filename=new_firmware_bin)
            sha256.load()

            warn_screen = self.manager.get_screen("WarningAfterAirgapUpdateScreen")

            fns = [
                partial(
                    warn_screen.update,
                    name=self.name,
                    key="sdcard",
                    value=path,
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

            self.set_screen(name="WarningAfterAirgapUpdateScreen", direction="left")

        setattr(AirgapUpdateScreen, "on_load", on_load)

        self.make_grid(wid=f"{self.id}_grid", rows=1)

        self.make_file_chooser(
            wid=f"{self.id}_select",
            root_widget=f"{self.id}_grid",
            view_mode="icon",
            font_factor=44,
            on_load=getattr(AirgapUpdateScreen, "on_load"),
        )

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

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
                "DownloadBetaScreen",
                "AirgapUpdateScreen",
            ),
            on_update=getattr(AirgapUpdateScreen, "on_update"),
        )
