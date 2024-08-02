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
from src.utils.constants import get_name, get_version
from src.app.screens.base_screen import BaseScreen


class AboutScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="about_screen", name="AboutScreen", **kwargs)
        self.make_grid(wid="about_screen_grid", rows=1)
        self.src_code = "https://github.com/selfcustody/krux-installer"

        def _on_press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _on_release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            self.set_screen(name="MainScreen", direction="right")

        self.make_button(
            row=0,
            id="about_screen_button",
            root_widget="about_screen_grid",
            text="",
            markup=True,
            on_press=_on_press,
            on_release=_on_release,
        )

        def _on_ref_press(*args):
            self.debug(f"Calling Button::{args[0]}::on_ref_press")
            self.debug(f"Opening {args[1]}")
            webbrowser.open(args[1])

        self.ids["about_screen_button"].halign = "center"
        self.ids["about_screen_button"].valign = "center"

        setattr(self, "on_ref_press_about_screen_button", _on_ref_press)
        self.ids["about_screen_button"].bind(on_ref_press=_on_ref_press)

    def update(self, *args, **kwargs):
        """Update buttons from selected device/versions on related screens"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in (
            "KruxInstallerApp",
            "ConfigKruxInstaller",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(msg=f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            if value is not None:
                self.locale = value
                title = f"[b]{get_name()}[/b]"
                version = f"v{get_version()}"

                source = "".join(
                    [
                        "[color=#00AABB]",
                        f"[ref={self.src_code}]",
                        self.translate("Check source code"),
                        "[/ref]",
                        "[/color]",
                    ]
                )

                issues = "".join(
                    [
                        "[color=#00AABB]",
                        f"[ref={self.src_code}/issues]",
                        f"{self.translate("I found a bug")}!",
                        "[/ref]",
                        "[/color]",
                    ]
                )

                if f"{self.id}_button" in self.ids:
                    self.ids[f"{self.id}_button"].text = "\n".join(
                        [title, version, "", source, "", issues]
                    )
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        else:
            self.redirect_error(msg=f'Invalid key: "{key}"')
