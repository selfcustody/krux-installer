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
# pylint: disable=no-name-in-module
import re
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from src.utils.selector import Selector
from .base_screen import BaseScreen


class SelectVersionScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_version_screen", name="SelectVersionScreen", **kwargs
        )

    def clear(self):
        """Clear the list of children widgets buttons"""
        self.ids["select_version_screen_grid"].clear_widgets()

    def fetch_releases(self):
        """Build a set of buttons to select version"""
        self.clear()
        self.selector = Selector()

        # build a list of latest versions plus old_versions and back buttons
        current_versions = [
            self.selector.releases[0],
            self.selector.releases[-1],
            "old versions",
            "back",
        ]

        for count, label in enumerate(current_versions):
            sanitized = label.replace(".", "_").replace("/", "_").replace(" ", "_")
            obj = {
                "id": f"select_version_{sanitized}",
                "text": label,
                "markup": False,
                "i": count,
            }
            self.make_button(
                root_widget="select_version_screen_grid",
                template=obj,
                total=len(current_versions),
            )

        # add some data to old versions plus a back button
        old_versions = self.selector.releases[1:-2]
        old_versions.append("back")
        old_versions_widget = self.manager.get_screen("SelectOldVersionScreen")
        old_versions_widget.fetch_releases(old_versions)

    def make_on_press(self, wid: str):
        """Dynamically define a on_press action"""

        def _on_press():
            self.on_press(wid=wid)

        return _on_press

    def make_on_release(self, wid: str):
        """Dynamically define a on_release action"""

        def _on_release():
            if re.findall(r"^select_version_v\d+\_\d+\_\d$", wid):
                self.change_version(wid=wid)
                self.on_release(wid=wid)
                self.set_screen(name="MainScreen", direction="right")
            if wid == "select_version_odudex_krux_binaries":
                self.change_version(wid=wid)
                self.on_release(wid=wid)
                self.set_screen(name="MainScreen", direction="right")
            elif wid == "select_version_old_versions":
                self.on_release(wid=wid)
                self.set_screen(name="SelectOldVersionScreen", direction="left")
            elif wid == "select_version_back":
                self.on_release(wid=wid)
                self.set_screen(name="MainScreen", direction="right")

        return _on_release

    def change_version(self, wid: str):
        """Change version text on MainScreen"""
        version = self.ids[wid].text
        self.debug(f"on_release::{wid} = {version}")

        main_screen = self.manager.get_screen("MainScreen")
        main_select_version = main_screen.ids["main_select_version"]
        main_select_version.text = f"Version: [color=#00AABB]{version}[/color]"
        self.debug(f"{main_select_version}.text = {main_select_version.text}")
