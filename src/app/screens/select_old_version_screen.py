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
from functools import partial
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

    def register_button_methods(self, name: str):
        """Dynamic registering of on_press and on_release methods for a button"""

        def on_press(instance):
            self.set_background(
                wid=f"select_old_version_{name}", rgba=(0.5, 0.5, 0.5, 0.5)
            )

        def on_release(instance):
            self.set_background(wid=f"select_old_version_{name}", rgba=(0, 0, 0, 0))
            self.change_version(wid=f"select_old_version_{name}")
            self.set_screen(name="MainScreen", direction="right")

        on_press.__name__ = "on_press_%s" % name
        on_release.__name__ = "on_release_%s" % name

        setattr(self, on_press.__name__, on_press)
        setattr(self, on_release.__name__, on_release)

    def fetch_releases(self, old_versions: List[str]):
        """Build a set of buttons to select version"""
        if not "select_old_version_screen_grid" in self.ids:
            self.make_grid(
                wid="select_old_version_screen_grid", rows=len(old_versions) + 1
            )

        self.clear()

        for row, text in enumerate(old_versions):
            sanitized = text.replace(".", "_").replace("/", "_")
            self.register_button_methods(name=sanitized)

            self.make_button(
                row=row,
                id=f"select_old_version_{sanitized}",
                root_widget="select_old_version_screen_grid",
                text=text,
                markup=False,
                on_press=getattr(self, f"on_press_{sanitized}"),
                on_release=getattr(self, f"on_release_{sanitized}"),
            )

        self.make_button(
            row=len(old_versions) + 1,
            id=f"select_old_version_back",
            root_widget="select_old_version_screen_grid",
            text="Back",
            markup=False,
            on_press=self.on_press_back,
            on_release=self.on_release_back,
        )

    def change_version(self, wid: str):
        """Change version text on MainScreen"""
        version = self.ids[wid].text
        self.debug(f"on_release::{wid} = {version}")

        main_screen = self.manager.get_screen("MainScreen")
        main_select_version = main_screen.ids["main_select_version"]
        main_select_version.text = f"Version: [color=#00AABB]{version}[/color]"
        self.debug(f"{main_select_version}.text = {main_select_version.text}")

    def on_press_back(self, instance):
        self.set_background(wid="select_old_version_back", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_back(self, instance):
        self.set_background(wid="select_old_version_back", rgba=(0, 0, 0, 0))
        self.set_screen(name="SelectVersionScreen", direction="right")
