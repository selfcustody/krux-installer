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

from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from src.app.screens.base_screen import BaseScreen
from kivy_circular_progress_bar import CircularProgressBar


class FlashScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="flash_screen", name="FlashScreen", **kwargs)
        self.make_grid(wid="flash_screen_grid", rows=1)

        # progress_bar_label = Label(text="0.0%", valign="center", halign="center")
        progress_bar = CircularProgressBar(
            pos=(Window.width / 2 - 100, Window.height / 2)
        )
        progress_bar.widget_size = Window.width * 0.50
        progress_bar.progress_colour = (0, 1, 0.5, 0)
        progress_bar.thickness = 15
        progress_bar.cap_style = "square"

        progress_bar.id = "flash_screen_progress_bar"
        self.ids["flash_screen_grid"].add_widget(progress_bar)
        self.ids[progress_bar.id] = WeakProxy(progress_bar)

    def update(self, *args, **kwargs):
        key = kwargs.get("key")
        if key == "progress":
            self.ids["flash_screen_progress_bar"].value = kwargs.get("value")
