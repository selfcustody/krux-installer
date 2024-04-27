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

from .base_screen import BaseScreen


class MainScreen(BaseScreen):
    """Main screen is the 'Home' page"""

    def __init__(self, **kwargs):
        super().__init__(wid="main_screen", name="MainScreen", **kwargs)

    def before_goto_screen(self, name: str):
        """Action to be performed :method:`on_press` action"""
        wid = ""

        if name == "FlashScreen":
            wid = "main_flash_device"

        elif name == "WipeScreen":
            wid = "main_wipe_device"

        elif name == "SettingsScreen":
            wid = "main_settings"

        elif name == "AboutScreen":
            wid = "main_about"

        else:
            raise ValueError(f"Invalid {name} screen")

        self.on_press(wid=wid)

    def goto_screen(self, name: str, direction: str):
        """Action to be performed :method:`on_release` action"""
        wid = ""

        if name == "FlashScreen":
            wid = "main_flash_device"

        elif name == "WipeScreen":
            wid = "main_wipe_device"

        elif name == "SettingsScreen":
            wid = "main_settings"

        elif name == "AboutScreen":
            wid = "main_about"

        else:
            raise ValueError(f"Invalid {name} screen")

        self.on_release(wid=wid)
        self.set_screen(name=name, direction=direction)
