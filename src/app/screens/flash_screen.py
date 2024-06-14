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
import os
import sys
import math
import distro
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.uix.label import Label
from src.app.screens.base_screen import BaseScreen
from kivy_circular_progress_bar import CircularProgressBar
from src.utils.flasher import Flasher


class FlashScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="flash_screen", name="FlashScreen", **kwargs)
        self.firmware = None
        self.device = None

        self.make_grid(wid="flash_screen_grid", rows=1)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(Window.width, Window.height))

        progress_bar_label = Label(text="0.0%", valign="center", halign="center")
        progress_bar = CircularProgressBar(
            pos=(Window.width / 2 - 100, Window.height / 2)
        )
        progress_bar.widget_size = math.floor(Window.width * 0.50)
        progress_bar.progress_colour = (0, 1, 0.5, 0)
        progress_bar.thickness = 15
        progress_bar.cap_style = "square"

        progress_bar.id = "flash_screen_progress_bar"
        self.ids["flash_screen_grid"].add_widget(progress_bar)
        self.ids[progress_bar.id] = WeakProxy(progress_bar)

    def on_pre_enter(self):
        self.ids[f"{self.id}_grid"].clear_widgets()
        verifying_msg = self.translate("Preparing flash")

        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))

            if self.success:
                self.set_screen(name="UnzipStableScreen", direction="left")
            else:
                self.set_screen(name="MainScreen", direction="right")

        self.make_button(
            id=f"{self.id}_button",
            root_widget=f"{self.id}_grid",
            text=f"[size=32sp][color=#efcc00]{verifying_msg}[/color][/size]",
            markup=True,
            row=0,
            on_press=_press,
            on_release=_release,
        )

    def update(self, *args, **kwargs):
        key = kwargs.get("key")
        value = kwargs.get("value")

        if key == "firmware":
            self.firmware = kwargs.get("value")
            self.ids["flash_screen_button"].text = "\n".join(
                [
                    "[size=32sp][color=#efcc00]Firmware to flash[/color][/size]",
                    f"[size=14]{self.firmware}[/size]",
                ]
            )

        if key == "device":
            self.device = kwargs.get("value")

        if key == "progress":
            self.ids["flash_screen_progress_bar"].value = kwargs.get("value")
