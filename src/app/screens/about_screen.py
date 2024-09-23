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
import webbrowser
from functools import partial
from kivy.clock import Clock
from src.utils.constants import get_version
from src.app.screens.base_screen import BaseScreen


class AboutScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="about_screen", name="AboutScreen", **kwargs)
        self.src_code = (
            "https://selfcustody.github.io/krux/getting-started/installing/from-gui/"
        )

        self.make_grid(wid="about_screen_grid", rows=1)

        def on_ref_press(*args):
            self.debug(f"Calling Button::{args[0]}::on_ref_press")
            self.debug(f"Opening {args[1]}")

            if args[1] == "Back":
                self.set_screen(name="MainScreen", direction="right")

            if args[1] == "X":
                webbrowser.open("https://x.com/selfcustodykrux")

            if args[1] == "SourceCode":
                webbrowser.open(self.src_code)

        self.make_button(
            row=0,
            wid=f"{self.id}_label",
            text="",
            root_widget=f"{self.id}_grid",
            font_factor=24,
            halign=None,
            on_press=None,
            on_release=None,
            on_ref_press=on_ref_press,
        )
        self.ids[f"{self.id}_label"].halign = "justify"

        fns = [
            partial(self.update, name=self.name, key="canvas"),
            partial(self.update, name=self.name, key="locale", value=self.locale),
        ]

        for fn in fns:
            Clock.schedule_once(fn, 0)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons from selected device/versions on related screens"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "locale":
                setattr(self, "locale", value)
                follow = self.translate("follow us on X")
                back = self.translate("Back")

                self.ids[f"{self.id}_label"].text = "".join(
                    [
                        f"[ref=SourceCode][b]v{get_version()}[/b][/ref]",
                        "\n",
                        "\n",
                        f"{follow}: ",
                        "[color=#00AABB]",
                        "[ref=X][u]@selfcustodykrux[/u][/ref]",
                        "[/color]",
                        "\n",
                        "\n",
                        "[color=#00FF00]",
                        "[ref=Back]",
                        f"[u]{back}[/u]",
                        "[/ref]",
                        "[/color]",
                    ]
                )

        setattr(AboutScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("KruxInstallerApp", "ConfigKruxInstaller", "AboutScreen"),
            on_update=getattr(AboutScreen, "on_update"),
        )
