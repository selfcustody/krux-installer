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
wipe_screen.py
"""

from functools import partial
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from src.utils.flasher.wiper import Wiper
from src.app.screens.base_flash_screen import BaseFlashScreen


class WipeScreen(BaseFlashScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="wipe_screen", name="WipeScreen", **kwargs)
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def on_pre_enter(self):
        self.ids[f"{self.id}_grid"].clear_widgets()

        def on_print_callback(*args, **kwargs):
            text = " ".join(str(x) for x in args)
            text = text.replace(
                "\x1b[32m\x1b[1m[INFO]\x1b[0m", "[color=#00ff00] INFO [/color]"
            )
            text = text.replace(
                "\x1b[33mISP loaded", "[color=#efcc00]ISP loaded[/color]"
            )
            text = text.replace(
                "\x1b[33mInitialize K210 SPI Flash",
                "[color=#efcc00]Initialize K210 SPI Flash[/color]",
            )
            text = text.replace("Flash ID: \x1b[33m", "Flash ID: [color=#efcc00]")
            text = text.replace(
                "\x1b[0m, unique ID: \x1b[33m", "[/color], unique ID: [color=#efcc00]"
            )
            text = text.replace("\x1b[0m, size: \x1b[33m", "[/color], size: ")
            text = text.replace("\x1b[0m MB", "[/color] MB")
            text = text.replace("\x1b[0m", "")
            text = text.replace("\x1b[33m", "")
            text = text.replace(
                "[INFO] Erasing the whole SPI Flash",
                "[color=#00ff00] INFO [/color] [color=#efcc00] Erasing the whole SPI Flash [/color]",
            )

            if text.startswith("[color=#00ff00] INFO [/color]"):
                self.output.append(text)

            if "SPI Flash erased." in text:
                self.is_done = True

            self.ids[f"{self.id}_info"].text = "\n".join(self.output)
            self.info(text)

        def on_process_callback(
            file_type: str, iteration: int, total: int, suffix: str
        ):
            pass

        def on_trigger_callback(dt):
            pass

        setattr(WipeScreen, "on_print_callback", on_print_callback)
        setattr(WipeScreen, "on_process_callback", on_process_callback)
        setattr(WipeScreen, "on_trigger_callback", on_trigger_callback)

        self.make_label(
            wid=f"{self.id}_info",
            text="",
            root_widget=f"{self.id}_grid",
            markup=True,
            halign="justify",
        )

    def on_enter(self):
        """
        Event fired when the screen is displayed and the entering animation is complete.
        """
        if self.wiper is not None:
            self.output = []
            self.progress = ""
            self.is_done = False
            self.trigger = getattr(self.__class__, "on_trigger_callback")
            self.wiper.ktool.__class__.print_callback = getattr(
                self.__class__, "on_print_callback"
            )
            self.thread = partial(
                self.wiper.wipe,
                device=self.device,
                callback=getattr(self.__class__, "on_process_callback"),
            )
            self.thread.start()
        else:
            raise ValueError("Wiper isnt configured. Use `update` method first")

    def update(self, *args, **kwargs):
        """Update screen with firmware key. Should be called before `on_enter`"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "MainScreen",
            "WipeScreen",
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

        elif key == "device":
            self.device = value

        elif key == "wiper":
            self.wiper = Wiper()
            self.wiper.baudrate = value

        elif key == "progress":
            self.ids[f"{self.id}_button"].text = "\n".join(
                [
                    "[size=8sp]" "\n".join(self.output),
                    "[/size]",
                    self.progress,
                ]
            )

        else:
            raise ValueError(f'Invalid key: "{key}"')
