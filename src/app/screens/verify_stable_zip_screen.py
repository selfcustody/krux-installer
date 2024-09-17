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
from functools import partial
import typing
from kivy.clock import Clock
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
        self.make_grid(wid=f"{self.id}_grid", rows=1, resize_screen=True)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update widget from other screens"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "verify":
                assets_dir = VerifyStableZipScreen.get_destdir_assets()
                main_screen = self.manager.get_screen("MainScreen")

                verified = self.build_message_verify_sha256(
                    assets_dir=assets_dir, version=main_screen.version
                )

                verified += self.build_message_verify_signature(
                    assets_dir=assets_dir, version=main_screen.version
                )

                self.ids[f"{self.id}_label"].text = verified

        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("ConfigKruxInstaller", self.name),
            on_update=on_update,
        )

    # pylint: disable=unused-argument
    def on_pre_enter(self, *args):
        self.ids[f"{self.id}_grid"].clear_widgets()

        def on_ref_press(*args):
            if args[1] == "Proceed":
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

            if args[1] == "Back":
                self.set_screen(name="MainScreen", direction="right")

        verifying_msg = self.translate("Verifying integrity and authenticity")
        self.make_button(
            row=0,
            wid=f"{self.id}_label",
            root_widget=f"{self.id}_grid",
            text=f"[color=#efcc00]{verifying_msg}[/color]",
            font_factor=48,
            halign="justify",
            on_press=None,
            on_release=None,
            on_ref_press=on_ref_press,
        )

    # pylint: disable=unused-argument
    def on_enter(self, *args, **kwargs):
        fn = partial(self.update, name=self.name, key="verify")
        Clock.schedule_once(fn)

    def verify_sha256(
        self, assets_dir: str, version: str
    ) -> typing.Tuple[str, str, bool]:
        """Do the verification when entering on screen"""
        # verify integrity
        sha256_0 = Sha256Verifyer(filename=f"{assets_dir}/krux-{version}.zip")
        sha256_1 = Sha256CheckVerifyer(
            filename=f"{assets_dir}/krux-{version}.zip.sha256.txt"
        )

        sha256_0.load()
        sha256_1.load()
        hash_0 = sha256_0.data.split(" ", maxsplit=1)[0]
        hash_1 = sha256_1.data.split(" ", maxsplit=1)[0]
        return (hash_0, hash_1, sha256_0.verify(hash_1))

    @staticmethod
    def prettyfy_hash(msg: str) -> str:
        """Slice strings, two by two, to better visualization"""
        splitted = [msg[i : i + 2] for i in range(0, len(msg), 2)]
        subsets = [
            "   ".join(splitted[i : i + 16]) for i in range(0, len(splitted), 16)
        ]
        return "\n".join(subsets)

    def build_message_verify_sha256(self, assets_dir: str, version: str) -> str:
        """Create a message which user can assert the integrity verification"""
        # memorize result
        verify = self.verify_sha256(assets_dir=assets_dir, version=version)
        hash_0 = verify[0]
        hash_1 = verify[1]
        checksummed = verify[2]

        self.success = checksummed

        filepath = os.path.join(assets_dir, f"krux-{version}.zip")
        integrity_msg = self.translate("Integrity verification")
        computed_msg = self.translate("computed hash from")
        provided_msg = self.translate("provided hash from")
        hash_color = ""
        hash_msg = ""
        sha_0 = VerifyStableZipScreen.prettyfy_hash(hash_0)
        sha_1 = VerifyStableZipScreen.prettyfy_hash(hash_1)

        if checksummed:
            hash_color = "#00FF00"
            hash_msg = self.translate("SUCCESS")
        else:
            hash_color = "#FF0000"
            hash_msg = self.translate("FAILED")

        return "".join(
            [
                f"[u]{integrity_msg.upper()}[/u]: ",
                f"[b][color={hash_color}]{hash_msg}[/color][/b]",
                "\n",
                "\n",
                f"[b]{computed_msg} [color=#777777]{filepath}[/color][/b]",
                "\n",
                sha_0,
                "\n",
                "\n",
                f"[b]{provided_msg} [color=#777777]{filepath}.sha256.txt[/color][/b]",
                "\n",
                sha_1,
                "\n",
                "\n",
            ]
        )

    def verify_signature(self, assets_dir: str, version: str) -> bool | str:
        """Verify official release's signature"""
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
        return sig_verifyer.verify()

    def build_message_verify_signature(self, assets_dir: str, version: str) -> str:
        """Create a message which user can assert authenticity the verification"""
        checksig = self.verify_signature(assets_dir=assets_dir, version=version)
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

        if checksig:
            sig_color = "#00FF00"
            res_msg = good_msg
        else:
            sig_color = "#FF0000"
            res_msg = bad_msg

        return "".join(
            [
                f"[u]{authenticity_msg.upper()}[/u]: ",
                f"[b][color={sig_color}]{res_msg} {sig_msg}[/color][/b]",
                "\n",
                "\n",
                installed_msg,
                "\n",
                check_msg,
                "\n",
                "\n",
                "[b]",
                f"openssl sha256< [color=#777777]{filepath}[/color] -binary | \\",
                "\n"
                f"openssl pkeyutl -verify -pubin -inkey [color=#777777]{pempath}[/color] \\",
                "\n",
                f"-sigfile [color=#777777]{filepath}.sig[/color]",
                "[/b]",
                "\n",
                "\n",
                f"[ref=Proceed][color=#00ff00][u]{proceed}[/u][/ref][/color]",
                "             ",
                f"[ref=Back][color=#ff0000][u]{back}[/u][/ref][/color]",
                "[/b]",
            ]
        )
