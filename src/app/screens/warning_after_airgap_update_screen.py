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
from kivy.app import App
from kivy.clock import Clock
from src.app.screens.base_screen import BaseScreen


class WarningAfterAirgapUpdateScreen(BaseScreen):
    """WarningAfterAirgapUpdateScreen warns user to insert it's FAT32 formatted SDCard"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="warning_after_airgap_update_screen",
            name="WarningAfterAirgapUpdateScreen",
            **kwargs,
        )

        self.sdcard = ""
        self.firmware_hash = ""

        self.make_grid(wid=f"{self.id}_grid", rows=2, resize_canvas=True)
        self.make_subgrid(
            wid=f"{self.id}_subgrid", rows=2, root_widget=f"{self.id}_grid"
        )

        self.build_upper_button()
        self.build_lower_button()

        # load canvas
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def build_upper_button(self):
        """Build the upper button screen"""

        def on_ref_press(*args):
            if args[1] == "MainScreen":
                self.set_screen(name="MainScreen", direction="right")

            if args[1] == "Quit":
                App.get_running_app().stop()

        self.make_image(
            wid=f"{self.id}_done",
            source=self.done_img,
            root_widget=f"{self.id}_subgrid",
        )

        self.make_button(
            row=1,
            wid=f"{self.id}_menu",
            text="",
            font_factor=32,
            root_widget=f"{self.id}_subgrid",
            halign="center",
            on_press=None,
            on_release=None,
            on_ref_press=on_ref_press,
        )

    def build_lower_button(self):
        """Build the lower button screen"""
        self.make_button(
            row=0,
            wid=f"{self.id}_label",
            text="",
            font_factor=36,
            halign=None,
            root_widget=f"{self.id}_grid",
            on_press=None,
            on_release=None,
            on_ref_press=None,
        )
        # self.ids[f"{self.id}_label"].halign = "cent"

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            # Check locale
            if key == "locale":
                setattr(self, "locale", value)
                self.ids[f"{self.id}_label"].text = self.make_label_text()

            if key == "sdcard":
                setattr(self, "sdcard", value)

            if key == "hash":
                setattr(self, "firmware_hash", value)

            if key == "label":
                self.ids[f"{self.id}_menu"].text = self.make_upper_label_text()
                self.ids[f"{self.id}_label"].text = self.make_lower_label_text()

        setattr(WarningAfterAirgapUpdateScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "AirgapUpdateScreen",
                "WarningAfterAirgapUpdateScreen",
            ),
            on_update=getattr(WarningAfterAirgapUpdateScreen, "on_update"),
        )

    def make_upper_label_text(self):
        """
        Create a warning message where it's content is about
        where ther firmware was placed
        """
        copied = self.translate("have been copied to")
        back = self.translate("Back")
        _quit = self.translate("Quit")
        return "".join(
            [
                f".bin and .sig files {copied}",
                "\n",
                f"[color=#efcc00]{self.sdcard}[/color].",
                "\n",
                "\n",
                "[color=#ff0000]",
                f"[u][ref=Quit]{_quit}[/ref][/u]",
                "[/color]",
                "        ",
                "[color=#00ff00]",
                f"[u][ref=MainScreen]{back}[/ref][/u]",
                "[/color]",
            ]
        )

    def make_lower_label_text(self):
        """
        Create a warning message where it's content is about
        the airgapped procedure to update firmware onto device
        """
        insert = self.translate(
            "Insert the SDcard into your device and reboot it to update"
        )

        return "".join(
            [
                f"* {insert}.",
                "\n",
                "\n",
                "* You should see this computed hash on device screen:",
                "\n",
                "\n",
                "[color=#efcc00]",
                WarningAfterAirgapUpdateScreen.prettyfy_hash(self.firmware_hash),
                "[/color]",
            ]
        )

    @staticmethod
    def prettyfy_hash(msg: str) -> str:
        """Slice strings, two by two, to better visualization"""
        splitted = [msg[i : i + 2] for i in range(0, len(msg), 2)]
        subsets = [
            "   ".join(splitted[i : i + 16]) for i in range(0, len(splitted), 16)
        ]
        return "\n".join(subsets)
