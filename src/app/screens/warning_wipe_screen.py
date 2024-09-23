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
from functools import partial
from kivy.clock import Clock
from src.app.screens.base_screen import BaseScreen


class WarningWipeScreen(BaseScreen):
    """WarningWipeScreen warns user about the wipe procedure"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="warning_wipe_screen",
            name="WarningWipeScreen",
            **kwargs,
        )

        self.make_grid(wid=f"{self.id}_grid", rows=2, resize_canvas=True)

        self.make_image(
            wid=f"{self.id}_warn",
            source=self.warn_img,
            root_widget=f"{self.id}_grid",
        )

        def on_ref_press(*args):
            if args[1] == "WipeScreen":
                partials = []
                main_screen = self.manager.get_screen("MainScreen")
                wipe_screen = self.manager.get_screen(args[1])
                baudrate = WarningWipeScreen.get_baudrate()
                partials.append(
                    partial(
                        wipe_screen.update,
                        name=self.name,
                        key="device",
                        value=main_screen.device,
                    )
                )
                partials.append(
                    partial(
                        wipe_screen.update,
                        name=self.name,
                        key="wiper",
                        value=baudrate,
                    )
                )

                for fn in partials:
                    print(fn)
                    Clock.schedule_once(fn, 0)

                self.set_screen(name=args[1], direction="left")

            if args[1] == "MainScreen":
                self.set_screen(name="MainScreen", direction="right")

        self.make_button(
            row=0,
            wid=f"{self.id}_label",
            text="",
            font_factor=48,
            halign=None,
            root_widget=f"{self.id}_grid",
            on_press=None,
            on_release=None,
            on_ref_press=on_ref_press,
        )

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    # pylint: disable=unused-argument
    def on_enter(self, *args, **kwargs):
        self.ids[f"{self.id}_label"].text = self.make_label_text()

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "locale":
                self.ids[f"{self.id}_label"].text = self.make_label_text()

        setattr(WarningWipeScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "MainScreen",
                "WarningWipeScreen",
            ),
            on_update=getattr(WarningWipeScreen, "on_update"),
        )

    def make_label_text(self):
        """Make a warning message about wipe procedure"""
        full_wipe = self.translate(
            "You are about to initiate a FULL WIPE of this device"
        )
        operation = self.translate("This operation will")
        erase = self.translate("Permanently erase all saved data")
        remove = self.translate("Remove the existing firmware")
        render = self.translate(
            "Render the device non-functional until new firmware is re-flashed"
        )
        proceed = self.translate("Proceed")
        back = self.translate("Back")

        return "".join(
            [
                "[color=#EFCC00]",
                full_wipe,
                "[/color]",
                "\n",
                "\n",
                f"{operation}:",
                "\n",
                f"* {erase}",
                "\n",
                f"* {remove}",
                "\n",
                f"* {render}",
                "\n",
                "\n",
                "[color=#00FF00]",
                f"[ref=WipeScreen][u]{proceed}[/u][/ref]",
                "[/color]",
                "        ",
                "[color=#FF0000]",
                f"[ref=MainScreen][u]{back}[/u][/ref]",
                "[/color]",
            ]
        )
