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
from kivy.uix.label import Label
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

        self.version = None

        self.make_grid(wid=f"{self.id}_grid", rows=3)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(Window.width, Window.height))

        # Sha256sum verification
        sha256_label = Label(
            text="[size=32sp][color=#efcc00]Verifying integrity...[/color][/size]",
            markup=True,
            valign="center",
            halign="center",
        )
        sha256_label.id = f"{self.id}_sha256_label"
        self.ids[f"{self.id}_grid"].add_widget(sha256_label)
        self.ids[sha256_label.id] = WeakProxy(sha256_label)

        # Signature verification
        sig_label = Label(
            text="[size=32sp][color=#efcc00]Verifying authenticity...[/color][/size]",
            markup=True,
            valign="center",
            halign="center",
        )
        sig_label.id = f"{self.id}_sig_label"
        self.ids[f"{self.id}_grid"].add_widget(sig_label)
        self.ids[sig_label.id] = WeakProxy(sig_label)

    def on_enter(self):
        assets_dir = App.get_running_app().config.get("destdir", "assets")
        main_screen = self.manager.get_screen("MainScreen")

        # verify integrity
        sha256_data_0 = Sha256Verifyer(
            filename=f"{assets_dir}/krux-{main_screen.version}.zip"
        )
        sha256_data_1 = Sha256CheckVerifyer(
            filename=f"{assets_dir}/krux-{main_screen.version}.zip.sha256.txt"
        )

        sha256_data_0.load()
        sha256_data_1.load()
        checksum = sha256_data_0.verify(sha256_data_1.data)

        self.ids[f"{self.id}_sha256_label"].text = "\n".join(
            [
                f"[size=18sp][color=#efcc00]Integrify verification:[/size][/color]",
                "",
                f"[b]{assets_dir}/krux-{main_screen.version}.zip[/b]:",
                f"[color={"#00FF00" if checksum else "#FF0000"}]{sha256_data_0.data}[/color]",
                "",
                f"[b]{assets_dir}/krux-{main_screen.version}.zip.sha256.txt[/b]:",
                f"[color={"#00FF00" if checksum else "#FF0000"}]{sha256_data_1.data}[/color]",
                "",
                f"Result: [b]{"SUCCESS" if checksum else "FAILED"}[/b]",
            ]
        )

        # verify signature
        signature = SigCheckVerifyer(
            filename=f"{assets_dir}/krux-{main_screen.version}.zip.sig"
        )
        publickey = PemCheckVerifyer(filename=f"{assets_dir}/selfcustody.pem")
        signature.load()
        publickey.load()
        sig_verifyer = SigVerifyer(
            filename=f"{assets_dir}/krux-{main_screen.version}.zip",
            regexp=r"^.*\.zip$",
            signature=signature.data,
            pubkey=publickey.data,
        )
        sig_verifyer.load()
        checksig = sig_verifyer.verify()

        self.ids[f"{self.id}_sig_label"].text = "\n".join(
            [
                "[size=18sp][color=#efcc00]Authenticiy verification:[/color][/size]",
                "",
                f"Binary: [b]{assets_dir}/krux-{main_screen.version}.zip[/b]:",
                "",
                f"Signature: [b]{assets_dir}/krux-{main_screen.version}.zip.sig[/b]:",
                "",
                f"Public key: [b]{assets_dir}/selfcustody.pem[/b]:",
                "",
                f"Result: [b]{"GOOD" if checksig else "BAD"} SIGNATURE[/b]",
            ]
        )

        # Create OK or Back button
        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            self.set_screen(name="MainScreen", direction="right")

        # Build OK button
        btn = Button(
            text=f"[size=32sp][b]{"Proceed" if checksum and checksig else "Re-download"}[/b][/size]",
            markup=True,
            font_size=Window.size[0] // 30,
            background_color=(0, 0, 0, 1),
            size_hint=(1, None),
        )
        btn.id = f"{self.id}_{"proceed" if checksum and checksig else "redownload"}"
        self.ids[f"{self.id}_grid"].add_widget(btn)
        self.ids[btn.id] = WeakProxy(btn)
        btn.bind(on_press=_press)
        btn.bind(on_release=_release)
        setattr(self, f"on_press_{btn.id}", _press)
        setattr(self, f"on_release_{btn.id}", _release)
