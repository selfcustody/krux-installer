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
from typing import List
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from src.utils.selector import Selector
from .base_screen import BaseScreen


class SelectOldVersionScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_old_version_screen", name="SelectOldVersionScreen", **kwargs
        )

    def clear(self):
        """Clear the list of children widgets buttons"""
        self.ids["select_old_version_screen_grid"].clear_widgets()

    def fetch_releases(self, old_versions: List[str]):
        """Build a set of buttons to select version"""
        self.clear()
        for count, label in enumerate(old_versions):
            sanitized = label.replace(".", "_").replace("/", "_").replace(" ", "_")
            obj = {
                "id": f"select_version_{sanitized}",
                "text": label,
                "markup": False,
                "i": count,
            }
            self.make_button(
                root_widget="select_old_version_screen_grid",
                template=obj,
                total=len(old_versions),
            )

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
            elif wid == "select_old_version_back":
                self.on_release(wid=wid)
                self.set_screen(name="SelectVersionScreen", direction="right")

        return _on_release

    def change_version(self, wid: str):
        """Change version text on MainScreen"""
        version = self.ids[wid].text
        self.debug(f"on_release::{wid} = {version}")

        main_screen = self.manager.get_screen("MainScreen")
        main_select_version = main_screen.ids["main_select_version"]
        main_select_version.text = f"Version: [color=#00AABB]{version}[/color]"
        self.debug(f"{main_select_version}.text = {main_select_version.text}")
