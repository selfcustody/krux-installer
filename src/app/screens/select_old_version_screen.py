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

    def on_fetch_releases(self, old_versions: List[str]):
        """Build a set of buttons to select version"""
        self.clear()
        for count, label in enumerate(old_versions):
            self._make_button(text=label, i=count, n=len(old_versions))

    def _make_button(self, text: str, i: int, n: int):
        """Build a general button"""
        btn = Button(
            text=text,
            font_size=Window.size[0] // 25,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )

        sanitized = text.replace(" ", "_").replace("//", "_")
        btn_wid = f"select_old_version_{sanitized}"

        btn.on_press = self._make_before_goto_screen(wid=btn_wid)
        btn.on_release = self._make_goto_screen(wid=btn_wid)
        btn.x = 0
        btn.y = (Window.size[1] / n) * i
        btn.width = Window.size[0]
        btn.height = Window.size[1] / n

        self.ids["select_old_version_screen_grid"].add_widget(btn)
        self.ids[btn_wid] = WeakProxy(btn)

        with self.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            Line(width=0.5, rectangle=(btn.x, btn.y, btn.width, btn.height))
            i = i + 1

        return btn

    def _make_before_goto_screen(self, wid: str):
        """Dynamically define a on_press action"""

        def _on_press():
            self.on_press(wid=wid)

        return _on_press

    def _make_goto_screen(self, wid: str):
        """Dynamically define a on_release action"""

        def _on_release():
            if re.findall(r"v\d+\.\d+\.\d", wid):
                self.on_release(wid=wid)
                self.set_screen(name="FlashScreen", direction="right")
            elif wid == "select_old_version_back":
                self.on_release(wid=wid)
                self.set_screen(name="SelectVersionScreen", direction="right")

        return _on_release
