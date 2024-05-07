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
import typing
from kivy.app import App
from kivy.cache import Cache
from .base_screen import BaseScreen
from src.utils.selector import VALID_DEVICES


class MainScreen(BaseScreen):
    """Main screen is the 'Home' page"""

    def __init__(self, **kwargs):
        super().__init__(wid="main_screen", name="MainScreen", **kwargs)

        # Prepare some variables
        self.device = "select a new one"
        self.version = "v24.03.0"
        self.will_flash = False
        self.will_wipe = False

        # Build grid where buttons will be placed
        self.make_grid(wid="main_screen_grid", rows=6)

        # Build buttons to be placed in GridLayout
        self.make_button(
            row=0,
            id="main_select_device",
            root_widget="main_screen_grid",
            text=f"Device: [color=#00AABB]{self.device}[/color]",
            markup=True,
            on_press=self.on_press_select_device,
            on_release=self.on_release_select_device,
        )

        self.make_button(
            row=1,
            id="main_select_version",
            root_widget="main_screen_grid",
            text=f"Version: [color=#00AABB]{self.version}[/color]",
            markup=True,
            on_press=self.on_press_select_version,
            on_release=self.on_release_select_version,
        )

        self.make_button(
            row=2,
            id="main_flash",
            root_widget="main_screen_grid",
            text=f"[color={"#FFFFFF" if self.will_flash else "#333333"}]Flash[/color]",
            markup=True,
            on_press=self.on_press_flash,
            on_release=self.on_release_flash,
        )

        self.make_button(
            row=3,
            id="main_wipe",
            root_widget="main_screen_grid",
            text=f"[color={"#FFFFFF" if self.will_wipe else "#333333"}]Wipe[/color]",
            markup=True,
            on_press=self.on_press_wipe,
            on_release=self.on_release_wipe,
        )

        self.make_button(
            row=4,
            id="main_settings",
            root_widget="main_screen_grid",
            text="Settings",
            markup=False,
            on_press=self.on_press_settings,
            on_release=self.on_release_settings,
        )

        self.make_button(
            row=5,
            id="main_about",
            root_widget="main_screen_grid",
            text="About",
            markup=False,
            on_press=self.on_press_about,
            on_release=self.on_release_about,
        )

    def update(self, *args, **kwargs):
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        self.debug(f"Updating MainScreen from {name}...")

        if key == "device":
            self.device = value
            self.debug(f"device = {value}")
            self.ids["main_select_device"].text = (
                f"Device: [color=#00AABB]{value}[/color]"
            )

        if key == "version":
            self.version = value
            self.debug(f"version = {value}")
            self.ids["main_select_version"].text = (
                f"Version: [color=#00AABB]{value}[/color]"
            )

        if self.device in VALID_DEVICES:
            self.will_flash = True
            self.debug(f"will_flash = {self.will_flash}")

            self.will_wipe = True
            self.debug(f"will_wipe = {self.will_wipe}")

            self.ids["main_flash"].text = "[color=#00FF00]Flash[/color]"
            self.debug(f"main_flash.text = {self.ids["main_flash"].text}")

            self.ids["main_wipe"].text = "[color=#00FF00]Wipe[/color]"
            self.debug(f"main_wipe.text = {self.ids["main_wipe"].text}")
        else:
            self.will_flash = False
            self.debug(f"will_flash = {self.will_flash}")

            self.will_wipe = False
            self.debug(f"will_wipe = {self.will_wipe}")

            self.ids["main_flash"].text = f"[color=#333333]Flash[/color]"
            self.debug(f"main_flash.text = {self.ids["main_flash"].text}")

            self.ids["main_wipe"].text = f"[color=#333333]Wipe[/color]"
            self.debug(f"main_wipe.text = {self.ids["main_wipe"].text}")

    def on_press_select_device(self, instance):
        self.set_background(wid="main_select_device", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_select_device(self, instance):
        self.set_background(wid="main_select_device", rgba=(0, 0, 0, 0))
        self.set_screen(name="SelectDeviceScreen", direction="left")

    def on_press_select_version(self, instance):
        self.set_background(wid="main_select_version", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_select_version(self, instance):
        select_version = self.manager.get_screen("SelectVersionScreen")
        select_version.clear()
        select_version.fetch_releases()
        self.set_background(wid="main_select_version", rgba=(0, 0, 0, 0))
        self.set_screen(name="SelectVersionScreen", direction="left")

    def on_press_flash(self, instance):
        if self.will_flash:
            self.set_background(wid="main_flash", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_flash(self, instance):
        if self.will_flash:
            self.set_background(wid="main_flash", rgba=(0, 0, 0, 0))
            self.set_screen(name="FlashScreen", direction="left")

    def on_press_wipe(self, instance):
        if self.will_wipe:
            self.set_background(wid="main_wipe", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_wipe(self, instance):
        if self.will_wipe:
            self.set_background(wid="main_wipe", rgba=(0, 0, 0, 0))
            self.set_screen(name="WipeScreen", direction="left")

    def on_press_settings(self, instance):
        self.set_background(wid="main_settings", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_settings(self, instance):
        self.set_background(wid="main_settings", rgba=(0, 0, 0, 0))
        App.get_running_app().open_settings()

    def on_press_about(self, instance):
        self.set_background(wid="main_about", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_about(self, instance):
        self.set_background(wid="main_about", rgba=(0, 0, 0, 0))
        self.set_screen(name="AboutScreen", direction="left")
