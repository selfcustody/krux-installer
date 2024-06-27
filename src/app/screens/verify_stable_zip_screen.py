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
from src.utils.verifyer.sha256_check_verifyer import Sha256CheckVerifyer
from src.utils.verifyer.sha256_verifyer import Sha256Verifyer
from src.utils.verifyer.sig_check_verifyer import SigCheckVerifyer
from src.utils.verifyer.sig_verifyer import SigVerifyer
from src.utils.verifyer.pem_check_verifyer import PemCheckVerifyer


class VerifyStableZipScreen(BaseScreen):
    """VerifyStableZipScreen check for sha256sum and siganture"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="verify_stable_zip_screen", name="VerifyStableZipScreen", **kwargs
        )
        self.success = False
        self.make_grid(wid=f"{self.id}_grid", rows=1)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(Window.width, Window.height))

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
        self.ids[f"{self.id}_grid"].clear_widgets()
        verifying_msg = self.translate("Verifying integrity and authenticity")

        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))

            if self.success:
                main_screen = self.manager.get_screen("MainScreen")
                unzip_screen = self.manager.get_screen("UnzipStableScreen")

                fns = [
                    partial(
                        unzip_screen.update,
                        name=self.name,
                        key="version",
                        value=main_screen.version,
                    ),
                    partial(
                        unzip_screen.update,
                        name=self.name,
                        key="device",
                        value=main_screen.device,
                    ),
                    partial(unzip_screen.update, name=self.name, key="clear"),
                    partial(unzip_screen.update, name=self.name, key="flash-button"),
                    partial(unzip_screen.update, name=self.name, key="airgap-button"),
                ]
                for fn in fns:
                    Clock.schedule_once(fn, 0)

                self.set_screen(name="UnzipStableScreen", direction="left")
            else:
                self.set_screen(name="MainScreen", direction="right")

        self.make_button(
            id=f"{self.id}_button",
            root_widget=f"{self.id}_grid",
            text=f"[size=32sp][color=#efcc00]{verifying_msg}[/color][/size]",
            markup=True,
            row=0,
            on_press=_press,
            on_release=_release,
        )

    def on_enter(self):
        assets_dir = App.get_running_app().config.get("destdir", "assets")
        main_screen = self.manager.get_screen("MainScreen")

        result_sha256 = self.verify_sha256(
            assets_dir=assets_dir, version=main_screen.version
        )
        self.ids[f"{self.id}_button"].text = result_sha256

        result_sign = self.verify_signature(
            assets_dir=assets_dir, version=main_screen.version
        )
        self.ids[f"{self.id}_button"].text += result_sign

    def verify_sha256(self, assets_dir: str, version: str) -> str:
        """Do the verification when entering on screen"""
        # verify integrity
        sha256_data_0 = Sha256Verifyer(filename=f"{assets_dir}/krux-{version}.zip")
        sha256_data_1 = Sha256CheckVerifyer(
            filename=f"{assets_dir}/krux-{version}.zip.sha256.txt"
        )

        sha256_data_0.load()
        sha256_data_1.load()
        checksum = sha256_data_0.verify(sha256_data_1.data)

        # memorize result
        self.success = checksum

        integrity_msg = self.translate("Integrity verification")
        success_msg = self.translate("SUCCESS")
        failed_msg = self.translate("FAILED")
        return "\n".join(
            [
                f"[size=20sp][color=#efcc00]{integrity_msg}:[/color][/size]",
                "",
                f"[size=16sp][b]{assets_dir}/krux-{version}.zip[/b][/size]",
                f"[size=14sp][color={"#00FF00" if checksum else "#FF0000"}]{sha256_data_0.data}[/color][/size]",
                "",
                f"[size=16sp][b]{assets_dir}/krux-{version}.zip.sha256.txt[/b][/size]",
                f"[size=14sp][color={"#00FF00" if checksum else "#FF0000"}]{sha256_data_1.data}[/color][/size]",
                f"[size=14sp]Result: [b]{success_msg if checksum else failed_msg}[/b][/size]",
                "",
                "",
            ]
        )

    def verify_signature(self, assets_dir: str, version: str) -> bool:
        # verify signature
        signature = SigCheckVerifyer(filename=f"{assets_dir}/krux-{version}.zip.sig")
        publickey = PemCheckVerifyer(filename=f"{assets_dir}/selfcustody.pem")
        signature.load()
        publickey.load()
        sig_verifyer = SigVerifyer(
            filename=f"{assets_dir}/krux-{version}.zip",
            regexp=r"^.*\.zip$",
            signature=signature.data,
            pubkey=publickey.data,
        )
        sig_verifyer.load()
        checksig = sig_verifyer.verify()

        # memorize result
        self.success = self.success and checksig

        authenticity_msg = self.translate("Authenticity verification")
        good_msg = self.translate("GOOD")
        bad_msg = self.translate("BAD")
        sig_msg = self.translate("SIGNATURE")
        installed_msg = self.translate("If you have openssl installed on your system")
        check_msg = self.translate("you can check manually with the following command")
        return "\n".join(
            [
                f"[size=20sp][color=#efcc00]{authenticity_msg}:[/color][/size]",
                "",
                f"[size=16sp]Result: [b]{good_msg if checksig else bad_msg} {sig_msg}[/b][/size]",
                "",
                f"[size=16sp]{installed_msg}[/size]",
                f"[size=16sp]{check_msg}:[/size]",
                "",
                f"[color=#00ff00][size=14sp]openssl sha256< {assets_dir}/krux-{version}.zip -binary | \\",
                f"openssl pkeyutl -verify -pubin -inkey {assets_dir}/selfcustody.pem \\",
                f"-sigfile {assets_dir}/krux-{version}.zip.sig[/size][/color]",
            ]
        )
