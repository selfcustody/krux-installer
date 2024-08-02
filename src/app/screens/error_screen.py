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
error_screen.py
"""
import traceback
from functools import partial
from typing import Text
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.app import App
from kivy.cache import Cache
from src.app.screens.base_screen import BaseScreen
from src.utils.selector import Selector
from src.i18n import T


class ErrorScreen(BaseScreen):
    """
    CheckInternetConnectionScreen will check internet connection and get the
    latest release if ok
    """

    def __init__(self, **kwargs):
        super().__init__(
            wid="error_screen",
            name="ErrorScreen",
            **kwargs,
        )
        self.src_code = "https://github.com/selfcustody/krux-installer"

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)

        # START of on_press buttons
        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=f"{instance.id}", rgba=(0, 0, 0, 1))
            self.set_screen(name="GreetingsScreen", direction="right")

        self.make_button(
            row=0,
            id=f"{self.id}_button",
            root_widget=f"{self.id}_grid",
            text="",
            markup=True,
            on_press=_press,
            on_release=_release,
        )
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def update(self, *args, **kwargs):
        """
        In linux, will check for user permission on group
        dialout (debian-li ke) and uucp (archlinux-like) and
        add user to that group to allow sudoless flash
        """
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "CheckInternetConnectionScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "ErrorScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen: {name}")

        if key == "locale":
            self.locale = value

        elif key == "canvas":
            # prepare background
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        elif key == "error":
            self.error(str(value.__context__))
            stack = [msg for msg in str(value.__context__).split(":") if len(msg) < 80]

            self.ids[f"{self.id}_button"].text = "\n".join(
                [
                    f"[size=18sp][color=#ff0000]{stack[0]}[/color][/size]",
                    f"[size=16sp][color=#efcc00]{"\n".join(stack[1:])}[/color][/size]",
                    "",
                    "",
                    "[size=16sp]Report issue at",
                    "".join(
                        [
                            "[color=#00aabb]",
                            f"[ref={self.src_code}/issues/]",
                            f"{self.src_code}/issues",
                            "[/ref]",
                            "[/color]",
                        ]
                    ),
                    "[/size]",
                ]
            )
        else:
            exc_info = ValueError(f"Invalid key: '{key}'")
            fn = partial(self.update, name=self.name, key="error", value=exc_info)
            Clock.schedule_once(fn, 0)

    def on_enter(self):
        """Simple update your canvas"""
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)
