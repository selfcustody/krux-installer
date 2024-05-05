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

        # Build grid where buttons will be placed
        self.make_grid(wid="select_version_screen_grid", rows=4)

    def clear(self):
        """Clear the list of children widgets buttons"""
        self.ids["select_version_screen_grid"].clear_widgets()

    def fetch_releases(self):
        """Build a set of buttons to select version"""
        selector = Selector()

        # Build buttons to be placed in GridLayout
        self.make_button(
            row=0,
            id=f"select_version_latest",
            root_widget="select_version_screen_grid",
            text=selector.releases[0],
            markup=False,
            on_press=self.on_press_stable,
            on_release=self.on_release_stable,
        )

        self.make_button(
            row=1,
            id=f"select_version_beta",
            root_widget="select_version_screen_grid",
            text=selector.releases[-1],
            markup=False,
            on_press=self.on_press_beta,
            on_release=self.on_release_beta,
        )

        self.make_button(
            row=2,
            id=f"select_version_old",
            root_widget="select_version_screen_grid",
            text="Old versions",
            markup=False,
            on_press=self.on_press_old,
            on_release=self.on_release_old,
        )

        self.make_button(
            row=3,
            id=f"select_version_back",
            root_widget="select_version_screen_grid",
            text="Back",
            markup=False,
            on_press=self.on_press_back,
            on_release=self.on_release_back,
        )

        # add some data to old versions plus a back button
        old_versions = selector.releases[1:-2]
        old_versions_widget = self.manager.get_screen("SelectOldVersionScreen")
        old_versions_widget.fetch_releases(old_versions)

    def change_version(self, wid: str):
        """Change version text on MainScreen"""
        version = self.ids[wid].text
        self.debug(f"on_release::{wid} = {version}")

        main_screen = self.manager.get_screen("MainScreen")
        main_select_version = main_screen.ids["main_select_version"]
        main_select_version.text = f"Version: [color=#00AABB]{version}[/color]"
        self.debug(f"{main_select_version}.text = {main_select_version.text}")

    def on_press_stable(self, instance):
        self.set_background(wid="select_version_latest", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_stable(self, instance):
        self.set_background(wid="select_version_latest", rgba=(0, 0, 0, 0))
        self.change_version(wid="select_version_latest")
        self.set_screen(name="MainScreen", direction="right")

    def on_press_beta(self, instance):
        self.set_background(wid="select_version_beta", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_beta(self, instance):
        self.set_background(wid="select_version_beta", rgba=(0, 0, 0, 0))
        self.change_version(wid="select_version_beta")
        self.set_screen(name="MainScreen", direction="right")

    def on_press_old(self, instance):
        self.set_background(wid="select_version_old", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_old(self, instance):
        self.set_background(wid="select_version_old", rgba=(0, 0, 0, 0))
        self.set_screen(name="SelectOldVersionScreen", direction="left")

    def on_press_back(self, instance):
        self.set_background(wid="select_version_back", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_back(self, instance):
        self.set_background(wid="select_version_back", rgba=(0, 0, 0, 0))
        self.set_screen(name="MainScreen", direction="right")
