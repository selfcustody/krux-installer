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
from functools import partial
from kivy.clock import Clock
from kivy.cache import Cache
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from src.utils.selector import VALID_DEVICES
from .base_screen import BaseScreen


class SelectDeviceScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_device_screen", name="SelectDeviceScreen", **kwargs
        )

        # Build grid where buttons will be placed
        self.make_grid(wid="select_device_screen_grid", rows=6)

        # Build buttons to be placed in GridLayout
        self.make_button(
            row=0,
            id="select_device_m5stickv",
            root_widget="select_device_screen_grid",
            text="m5stickv",
            markup=False,
            on_press=self.on_press_m5stickv,
            on_release=self.on_release_m5stickv,
        )

        self.make_button(
            row=1,
            id="select_device_amigo",
            root_widget="select_device_screen_grid",
            text="amigo",
            markup=False,
            on_press=self.on_press_amigo,
            on_release=self.on_release_amigo,
        )

        self.make_button(
            row=2,
            id="select_device_dock",
            root_widget="select_device_screen_grid",
            text="dock",
            markup=False,
            on_press=self.on_press_dock,
            on_release=self.on_release_dock,
        )

        self.make_button(
            row=3,
            id="select_device_bit",
            root_widget="select_device_screen_grid",
            text="bit",
            markup=False,
            on_press=self.on_press_bit,
            on_release=self.on_release_bit,
        )

        self.make_button(
            row=4,
            id="select_device_yahboom",
            root_widget="select_device_screen_grid",
            text="yahboom",
            markup=False,
            on_press=self.on_press_yahboom,
            on_release=self.on_release_yahboom,
        )

        self.make_button(
            row=5,
            id="select_device_cube",
            root_widget="select_device_screen_grid",
            text="cube",
            markup=False,
            on_press=self.on_press_cube,
            on_release=self.on_release_cube,
        )

    def change_device(self, wid: str):
        """Change device text on MainScreen"""
        device = self.ids[wid].text
        self.debug(f"on_release::{wid} = {device}")

        main_screen = self.manager.get_screen("MainScreen")
        fn = partial(main_screen.update, name=self.name, key="device", value=device)
        Clock.schedule_once(fn, 0)

    def on_press_m5stickv(self, instance):
        self.set_background(wid="select_device_m5stickv", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_m5stickv(self, instance):
        self.set_background(wid="select_device_m5stickv", rgba=(0, 0, 0, 0))
        self.change_device(wid="select_device_m5stickv")
        self.set_screen(name="MainScreen", direction="right")

    def on_press_amigo(self, instance):
        self.set_background(wid="select_device_amigo", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_amigo(self, instance):
        self.set_background(wid="select_device_amigo", rgba=(0, 0, 0, 0))
        self.change_device(wid="select_device_amigo")
        self.set_screen(name="MainScreen", direction="right")

    def on_press_dock(self, instance):
        self.set_background(wid="select_device_dock", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_dock(self, instance):
        self.set_background(wid="select_device_dock", rgba=(0, 0, 0, 0))
        self.change_device(wid="select_device_dock")
        self.set_screen(name="MainScreen", direction="right")

    def on_press_bit(self, instance):
        self.set_background(wid="select_device_bit", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_bit(self, instance):
        self.set_background(wid="select_device_bit", rgba=(0, 0, 0, 0))
        self.change_device(wid="select_device_bit")
        self.set_screen(name="MainScreen", direction="right")

    def on_press_yahboom(self, instance):
        self.set_background(wid="select_device_yahboom", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_yahboom(self, instance):
        self.set_background(wid="select_device_yahboom", rgba=(0, 0, 0, 0))
        self.change_device(wid="select_device_yahboom")
        self.set_screen(name="MainScreen", direction="right")

    def on_press_cube(self, instance):
        self.set_background(wid="select_device_cube", rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release_cube(self, instance):
        self.set_background(wid="select_device_cube", rgba=(0, 0, 0, 0))
        self.change_device(wid="select_device_cube")
        self.set_screen(name="MainScreen", direction="right")
