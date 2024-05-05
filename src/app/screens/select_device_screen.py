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

        buttons = [
            {"id": f"select_device_{device}", "text": device, "markup": False, "i": i}
            for i, device in enumerate(VALID_DEVICES)
        ]
        for device in buttons:
            self.make_button(
                root_widget="select_device_screen_grid",
                template=device,
                total=len(VALID_DEVICES),
            )

    def make_on_press(self, wid: str):
        """Dynamically define a on_press action"""

        def _on_press():
            self.on_press(wid=wid)

        return _on_press

    def make_on_release(self, wid: str):
        """Dynamically define a on_release action"""

        def _on_release():
            self.change_device(wid=wid)
            self.on_release(wid=wid)
            self.set_screen(name="MainScreen", direction="right")

        return _on_release

    def change_device(self, wid: str):
        """Change device text on MainScreen"""
        device = self.ids[wid].text
        self.debug(f"on_release::{wid}={device}")

        main_screen = self.manager.get_screen("MainScreen")
        main_select_device = main_screen.ids["main_select_device"]

        main_select_device.text = f"Device: [color=#00AABB]{device}[/color]"
        self.debug(f"{main_select_device}.text = {main_select_device.text}")
