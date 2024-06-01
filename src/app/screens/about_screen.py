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
from .base_screen import BaseScreen


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

        title = f"[b]{get_name()}[/b]"
        version = f"v{get_version()}"
        source = f"[color=#00AABB][ref={self.src_code}]Check source code[/ref][/color]"
        issues = (
            f"[color=#00AABB][ref={self.src_code}/issues]I found a bug![/ref][/color]"
        )

        self.make_button(
            row=0,
            id=f"about_screen_button",
            root_widget="about_screen_grid",
            text="\n".join([title, version, "", source, "", issues]),
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

        setattr(self, f"on_ref_press_about_screen_button", _on_ref_press)
        self.ids["about_screen_button"].bind(on_ref_press=_on_ref_press)
