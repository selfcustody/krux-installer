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
from src.utils.selector import Selector
from .base_screen import BaseScreen


class SelectVersionScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_version_screen", name="SelectVersionScreen", **kwargs
        )

    def on_fetch_releases(self):
        self.selector = Selector()
        i = 0

        for version in self.selector.releases:
            btn = Button(
                text=version,
                font_size=Window.size[0] // 25,
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1),
            )

            btn_wid = f"select_version_{version}"
            btn.id = btn_wid

            btn.on_press = self._make_on_press(wid=btn_wid)
            btn.x = 0
            btn.y = (Window.size[1] / len(self.selector.releases)) * i
            btn.width = Window.size[0]
            btn.height = Window.size[1] / len(self.selector.releases)
            self.ids["select_version_screen_grid"].add_widget(btn)
            self.ids[btn_wid] = WeakProxy(btn)

            with self.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                Line(width=0.5, rectangle=(btn.x, btn.y, btn.width, btn.height))
                i = i + 1

    def _make_on_press(self, wid: str):
        """Dynamically define a on_press action"""

        def _on_press():
            self.on_press(wid=wid)

        return _on_press
