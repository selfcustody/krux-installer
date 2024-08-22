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
from kivy.uix.label import Label
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

        # instead make a button
        # create a ref text that instead redirect
        # to a web page, redirect to a screen
        def _on_ref_press(*args):
            self.debug(f"Calling ref::{args[0]}::on_ref_press")
            self.debug(f"Opening {args[1]}")

            if args[1] == "UnzipStableScreen":
                main_screen = self.manager.get_screen("MainScreen")
                u = self.manager.get_screen("UnzipStableScreen")

                fns = [
                    partial(
                        u.update,
                        name=self.name,
                        key="version",
                        value=main_screen.version,
                    ),
                    partial(
                        u.update, name=self.name, key="device", value=main_screen.device
                    ),
                    partial(u.update, name=self.name, key="clear"),
                    partial(u.update, name=self.name, key="flash-button"),
                    partial(u.update, name=self.name, key="airgap-button"),
                ]

                for fn in fns:
                    Clock.schedule_once(fn, 0)

                self.set_screen(name="UnzipStableScreen", direction="left")

            elif args[1] == "MainScreen":
                self.set_screen(name="MainScreen", direction="right")

        setattr(VerifyStableZipScreen, f"on_ref_press_{self.id}", _on_ref_press)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn)

    def update(self, *args, **kwargs):
        """Update widget from other screens"""

        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in ("ConfigKruxInstaller", "VerifyStableZipScreen"):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(f"Invalid screen name: {name}")
            return

        # Check locale
        if key == "locale":
            if value is not None:
                self.locale = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "canvas":
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        else:
            self.redirect_error(f'Invalid key: "{key}"')

    def on_pre_enter(self):
        self.ids[f"{self.id}_grid"].clear_widgets()
        verifying_msg = self.translate("Verifying integrity and authenticity")

        warning = Label(
            text="".join(
                [
                    f"[size={self.SIZE_MM}sp]",
                    "[color=#efcc00]",
                    verifying_msg,
                    "[/color]",
                    "[/size]",
                ]
            ),
            markup=True,
            valign="center",
            halign="left",
        )
        warning.id = f"{self.id}_label"
        self.ids[f"{self.id}_grid"].add_widget(warning)
        self.ids[warning.id] = WeakProxy(warning)
        self.ids[warning.id].bind(
            on_ref_press=getattr(VerifyStableZipScreen, f"on_ref_press_{self.id}")
        )

    def on_enter(self):
        assets_dir = VerifyStableZipScreen.get_destdir_assets()
        main_screen = self.manager.get_screen("MainScreen")

        result_sha256 = self.verify_sha256(
            assets_dir=assets_dir, version=main_screen.version
        )
        self.ids[f"{self.id}_label"].text = result_sha256

        result_sign = self.verify_signature(
            assets_dir=assets_dir, version=main_screen.version
        )
        self.ids[f"{self.id}_label"].text += result_sign

    def verify_sha256(self, assets_dir: str, version: str) -> str:
        """Do the verification when entering on screen"""
        # verify integrity
        sha256_data_0 = Sha256Verifyer(filename=f"{assets_dir}/krux-{version}.zip")
        sha256_data_1 = Sha256CheckVerifyer(
            filename=f"{assets_dir}/krux-{version}.zip.sha256.txt"
        )

        sha256_data_0.load()
        sha256_data_1.load()
        txt_hash_0 = sha256_data_0.data.split(" ")[0]
        txt_hash_1 = sha256_data_1.data.split(" ")[0]
        checksum = sha256_data_0.verify(txt_hash_1)

        # memorize result
        self.success = checksum

        filepath = os.path.join(assets_dir, f"krux-{version}.zip")
        integrity_msg = self.translate("Integrity verification")
        computed_msg = self.translate("computed hash from")
        provided_msg = self.translate("provided hash from")
        hash_color = ""
        hash_msg = ""

        if sys.platform in ("linux", "win32"):
            size = [self.SIZE_MP, self.SIZE_P, self.SIZE_PP]
        else:
            size = [self.SIZE_M, self.SIZE_MP, self.SIZE_P]

        # slice strings, two by two, to better visualization
        chunk_sha_0 = [txt_hash_0[i : i + 2] for i in range(0, len(txt_hash_0), 2)]
        chunk_sha_1 = [txt_hash_1[i : i + 2] for i in range(0, len(txt_hash_1), 2)]

        # if strings is greater than 16, split in a 2 subsets
        subset_sha_0 = [
            "   ".join(chunk_sha_0[i : i + 16]) for i in range(0, len(chunk_sha_0), 16)
        ]
        subset_sha_1 = [
            "   ".join(chunk_sha_1[i : i + 16]) for i in range(0, len(chunk_sha_1), 16)
        ]

        # join the 2 subsets with \n (next line) string
        sha_0 = "\n".join(subset_sha_0)
        sha_1 = "\n".join(subset_sha_1)

        if checksum:
            hash_color = "#00FF00"
            hash_msg = self.translate("SUCCESS")
        else:
            hash_color = "FF0000"
            hash_msg = self.translate("FAILED")

        return "".join(
            [
                f"[size={size[0]}sp]",
                f"[u]{integrity_msg.upper()}[/u]: ",
                f"[b][color={hash_color}]{hash_msg}[/color][/b]",
                "[/size]",
                "\n",
                "\n",
                f"[size={size[1]}sp]",
                f"[b]{computed_msg} [color=#777777]{filepath}[/color][/b]",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]{sha_0}[/size]",
                "\n",
                "\n",
                f"[size={size[1]}sp]",
                f"[b]{provided_msg} [color=#777777]{filepath}.sha256.txt[/color][/b]",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]{sha_1}[/size]",
                "\n",
                "\n",
                "\n",
            ]
        )

    def verify_signature(self, assets_dir: str, version: str) -> bool | str:
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
        proceed = self.translate("Proceed")
        back = self.translate("Back")
        filepath = os.path.join(assets_dir, f"krux-{version}.zip")
        pempath = os.path.join(assets_dir, "selfcustody.pem")

        if sys.platform in ("linux", "win32"):
            size = [self.SIZE_MP, self.SIZE_P]
        else:
            size = [self.SIZE_M, self.SIZE_MP]

        if checksig:
            sig_color = "#00FF00"
            res_msg = good_msg
        else:
            sig_color = "FF0000"
            res_msg = bad_msg

        return "".join(
            [
                f"[size={size[0]}sp]",
                f"[u]{authenticity_msg.upper()}[/u]: ",
                f"[b][color={sig_color}]{res_msg} {sig_msg}[/color][/b]",
                "[/size]",
                "\n",
                "\n",
                "\n",
                f"[size={size[1]}sp]{installed_msg}[/size]",
                "\n" f"[size={size[1]}sp]{check_msg}:[/size]",
                "\n",
                "\n",
                f"[size={size[1]}sp]",
                "[b]",
                f"openssl sha256< [color=#777777]{filepath}[/color] -binary | \\",
                "\n"
                f"openssl pkeyutl -verify -pubin -inkey [color=#777777]{pempath}[/color] \\",
                "\n",
                f"-sigfile [color=#777777]{filepath}.sig[/color]",
                "[/size]",
                "[/b]",
                "\n",
                "\n",
                f"[size={size[1]}sp][b][color=#{sig_color}]{res_msg} {sig_msg}[/b][/color][/size]",
                "\n",
                "\n",
                f"[size={size[0]}sp]",
                f"[ref=UnzipStableScreen][color=#00ff00]{proceed}[/ref][/color]",
                "             ",
                f"[ref=MainScreen][color=#ff0000]{back}[/ref][/color]",
                "[/b]",
                "[/size]",
            ]
        )
