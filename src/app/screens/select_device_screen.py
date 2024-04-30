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

        i = 0
        for device in VALID_DEVICES:
            btn = Button(
                text=device,
                font_size=Window.size[0] // 25,
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1),
            )

            btn_wid = f"select_device_{device}"
            btn.id = btn_wid

            btn.on_press = self._make_before_goto_screen(wid=btn_wid)
            btn.on_release = self._make_goto_screen(wid=btn_wid)
            btn.x = 0
            btn.y = (Window.size[1] / len(VALID_DEVICES)) * i
            btn.width = Window.size[0]
            btn.height = Window.size[1] / len(VALID_DEVICES)
            self.ids["select_device_screen_grid"].add_widget(btn)
            self.ids[btn_wid] = WeakProxy(btn)

            with self.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                Line(width=0.5, rectangle=(btn.x, btn.y, btn.width, btn.height))
                i = i + 1

    def _make_before_goto_screen(self, wid: str):
        """Dynamically define a on_press action"""

        def _on_press():
            self.on_press(wid=wid)

        return _on_press

    def _make_goto_screen(self, wid: str):
        """Dynamically define a on_release action"""

        def _on_release():
            self.on_release(wid=wid)
            self.set_screen(name="FlashScreen", direction="right")

        return _on_release
