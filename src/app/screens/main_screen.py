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
import typing
from kivy.app import App
from kivy.cache import Cache
from .base_screen import BaseScreen
from kivy.uix.gridlayout import GridLayout
from kivy.weakproxy import WeakProxy


class MainScreen(BaseScreen):
    """Main screen is the 'Home' page"""

    def __init__(self, **kwargs):
        super().__init__(wid="main_screen", name="MainScreen", **kwargs)

        # Prepare some variables
        self.device = "select a new one"
        self.version = "v24.03.0"
        self.willFlash = False
        self.willWipe = False

        # Build grid where buttons will be placed
        grid = GridLayout(cols=1)
        grid.id = "main_screen_grid"
        self.add_widget(grid)
        self.ids["main_screen_grid"] = WeakProxy(grid)

        # Build buttons to be placed in GridLayout
        buttons = [
            {
                "id": "main_select_device",
                "text": f"Device: [color=#00AABB]{self.device}[/color]",
                "markup": True,
                "i": 0,
            },
            {
                "id": "main_select_version",
                "text": f"Version: [color=#00AABB]{self.version}[/color]",
                "markup": True,
                "i": 1,
            },
            {
                "id": "main_flash",
                "text": f"[color={"#FFFFFF" if self.willFlash else "#333333"}]Flash[/color]",
                "markup": True,
                "i": 2,
            },
            {
                "id": "main_wipe",
                "text": "Wipe",
                "text": f"[color={"#FFFFFF" if self.willWipe else "#333333"}]Wipe[/color]",
                "markup": True,
                "i": 3,
            },
            {"id": "main_settings", "text": "Settings", "markup": False, "i": 4},
            {"id": "main_about", "text": "About", "markup": False, "i": 5},
        ]

        for btn in buttons:
            self.make_button(
                root_widget="main_screen_grid", template=btn, total=len(buttons)
            )

    def make_on_press(self, wid: str):
        """Build an action to be performed :method:`on_press` action"""

        def on_press():
            if wid in (
                "main_select_device",
                "main_select_version",
                "main_flash",
                "main_wipe",
                "main_settings",
                "main_about",
            ):
                self.on_press(wid=wid)
            else:
                raise ValueError(f"Invalid id screen: '{wid}'")

        return on_press

    def make_on_release(self, wid: str, direction: str = "left"):
        """Action to be performed :method:`on_release` action"""

        def on_release():
            if wid == "main_select_device":
                name = "SelectDeviceScreen"

            elif wid == "main_select_version":
                name = "SelectVersionScreen"
                self.manager.get_screen("SelectVersionScreen").fetch_releases()

            elif wid == "main_flash":
                name = "FlashScreen"

            elif wid == "main_wipe":
                name = "WipeScreen"

            elif wid == "main_settings":
                name = "SettingsScreen"

            elif wid == "main_about":
                name = "AboutScreen"

            else:
                raise ValueError(f"Invalid {name} screen")

            self.on_release(wid=wid)

            if name == "SettingsScreen":
                _app = App.get_running_app()
                _app.open_settings()
            else:
                self.set_screen(name=name, direction=direction)

        return on_release
