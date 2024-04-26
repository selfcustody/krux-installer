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
base_screen.py
"""
import typing
from kivy.uix.screenmanager import Screen
from src.utils.trigger import Trigger


class BaseScreen(Screen, Trigger):
    """Main screen is the 'Home' page"""

    def __init__(self, wid: str, name: str, **kwargs):
        super().__init__(**kwargs)
        self.id = wid
        self.name = name

    def on_press(self, wid: str):
        """General on_press method to change background of buttons"""
        msg = f"Button::{wid} clicked"
        self.debug(msg)
        self.set_background(wid=wid, rgba=(0.5, 0.5, 0.5, 0.5))

    def on_release(self, wid: str):
        """General on_release method to change background of buttons"""
        msg = f"Button::{wid} released"
        self.debug(msg)
        self.set_background(wid=wid, rgba=(0, 0, 0, 0))

    def set_background(self, wid: str, rgba: typing.Tuple[float, float, float, float]):
        """Changes the widget's background by it's id"""
        widget = self.ids[wid]
        msg = f"Button::{wid}.background_color={rgba}"
        self.debug(msg)
        widget.background_color = rgba

    def set_screen(self, name: str, direction: typing.Literal["left", "right"]):
        """Change to some screen registered on screen_manager"""
        msg = f"Switching to screen='{name}' by direction='{direction}'"
        self.debug(msg)
        self.manager.transition.direction = direction
        self.manager.current = name
