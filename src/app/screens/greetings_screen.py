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
greetings_screen.py
"""
import sys
from functools import partial
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.core.window import Window
from .base_screen import BaseScreen


class GreetingsScreen(BaseScreen):
    """GreetingsScreen show Krux logo"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="greetings_screen",
            name="GreetingsScreen",
            **kwargs,
        )

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)

        # Build logo
        self.make_image(
            wid=f"{self.id}_logo", root_widget=f"{self.id}_grid", source=self.logo_img
        )

    def update(self, *args, **kwargs):
        """Update to go to some screen (MainScreen or CheckPermissionsScreen)"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in ("GreetingsScreen", "KruxInstallerApp"):
            self.debug(f"Updating {self.name} from {name}")
        else:
            raise ValueError(f"Invalid screen: {name}")

        if key == "change_screen":
            if value is not None and value in (
                "MainScreen",
                "CheckPermissionsScreen",
                "CheckInternetConnectionScreen",
            ):
                self.set_screen(name=value, direction="left")
            else:
                raise ValueError(f"Invalid value for '{key}': {value}")

        elif key == "canvas":

            with self.canvas.before:
                Color(0, 0, 0)
                Rectangle(pos=(0, 0), size=Window.size)

        elif key == "check_permissions":
            # check platform and if is linux, go to CheckPermissionsScreen,
            # otherwise, go to MainScreen

            if sys.platform == "linux":
                fn = partial(
                    self.update,
                    name=self.name,
                    key="change_screen",
                    value="CheckPermissionsScreen",
                )

            elif sys.platform == "darwin" or sys.platform == "win32":
                fn = partial(
                    self.update,
                    name=self.name,
                    key="change_screen",
                    value="CheckInternetConnectionScreen",
                )

            else:
                raise RuntimeError(f"Not implemented for {sys.platform}")

            Clock.schedule_once(fn, 2.1)

        else:
            raise ValueError(f"Invalid key: '{key}'")

    def on_enter(self):
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)
