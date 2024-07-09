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
import math
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from src.app.screens.base_screen import BaseScreen
from kivy_circular_progress_bar import CircularProgressBar
from src.utils.flasher import Flasher


class FlashScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="flash_screen", name="FlashScreen", **kwargs)
        self.firmware = None
        self.baudrate = None
        self.make_grid(wid=f"{self.id}_grid", rows=1)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def on_pre_enter(self):
        self.ids[f"{self.id}_grid"].clear_widgets()
        verifying_msg = self.translate("Preparing flash")

        def on_print_callback(*args, **kwargs):
            self.info(f"print_callback arg: {args}")
            self.info(f"print_callback kwargs: {kwargs}")
            print()

        def on_process_callback(
            file_type: str, iteration: int, total: int, suffix: str
        ):
            self.info(f"file_type: {file_type}")
            self.info(f"iteration: {iteration}")
            self.info(f"total: {total}")
            self.info(f"suffix: {suffix}")
            print()

        setattr(FlashScreen, "on_print_callback", on_print_callback)
        setattr(FlashScreen, "on_process_callback", on_process_callback)

        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))
            self.ids[f"{self.id}_button"].text = ""

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            flasher = Flasher()
            flasher.firmware = self.firmware
            flasher.baudrate = self.baudrate
            flasher.ktool.__class__.print_callback = getattr(
                FlashScreen, "on_print_callback"
            )
            flasher.flash(callback=getattr(FlashScreen, "on_process_callback"))

        setattr(FlashScreen, f"on_press_{self.id}_button", _press)
        setattr(FlashScreen, f"on_release_{self.id}_button", _release)

        self.make_button(
            id=f"{self.id}_button",
            root_widget=f"{self.id}_grid",
            text=f"[size=32sp][color=#efcc00]{verifying_msg}[/color][/size]",
            markup=True,
            row=0,
            on_press=getattr(FlashScreen, f"on_press_{self.id}_button"),
            on_release=getattr(FlashScreen, f"on_release_{self.id}_button"),
        )

        progress_bar = CircularProgressBar(
            pos=(Window.width / 2 - 100, Window.height / 2)
        )
        progress_bar.widget_size = math.floor(Window.width * 0.50)
        progress_bar.progress_colour = (0, 1, 0.5, 0)
        progress_bar.thickness = 15
        progress_bar.cap_style = "square"

        progress_bar.id = f"{self.id}_progress_bar"
        self.ids[f"{self.id}_button"].add_widget(progress_bar)
        self.ids[progress_bar.id] = WeakProxy(progress_bar)

    def update(self, *args, **kwargs):
        """Update screen with firmware key. Should be called before `on_enter`"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "FlashScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen name: {name}")

        key = kwargs.get("key")
        value = kwargs.get("value")

        if key == "locale":
            self.locale = value

        elif key == "canvas":
            # prepare background
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        if key == "baudrate":
            self.baudrate = value

        elif key == "firmware":
            self.firmware = value
            self.ids["flash_screen_button"].text = "\n".join(
                [
                    "[size=32sp][color=#efcc00]Click on screen",
                    "to flash the firmware[/color][/size]",
                    f"[size=16]{self.firmware}[/size]",
                ]
            )

        if key == "progress":
            self.ids["flash_screen_progress_bar"].value = kwargs.get("value")
