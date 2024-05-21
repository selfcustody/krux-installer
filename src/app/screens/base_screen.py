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
from functools import partial
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.graphics import Color, Line
from kivy.uix.screenmanager import Screen
from src.utils.trigger import Trigger
from src.i18n import T
from src.utils.selector import VALID_DEVICES


class BaseScreen(Screen, Trigger):
    """Main screen is the 'Home' page"""

    def __init__(self, wid: str, name: str, **kwargs):
        super().__init__(**kwargs)
        self.id = wid
        self.name = name

        locale = App.get_running_app().config.get("locale", "lang")
        locale = locale.split(".")
        locale = f"{locale[0].replace("-", "_")}.{locale[1]}"
        self.locale = locale

    @property
    def locale(self) -> str:
        """Getter for locale property"""
        return self._locale

    @locale.setter
    def locale(self, value: bool):
        """Setter for locale property"""
        self.debug(f"locale = {value}")
        self._locale = value

    def translate(self, key: str) -> str:
        msg = T(key, locale=self.locale, module=self.id)
        self.debug(f"Translated '{key}' to '{msg}'")
        return msg

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

    def make_grid(self, wid: str, rows: int):
        """Build grid where buttons will be placed"""
        if not wid in self.ids:
            self.debug(f"Building GridLayout::{wid}")
            grid = GridLayout(cols=1, rows=rows)
            grid.id = wid
            self.add_widget(grid)
            self.ids[wid] = WeakProxy(grid)
        else:
            self.debug(f"GridLayout::{wid} already exist")

    def clear_grid(self, wid: str):
        """Clear GridLayout widget"""
        self.debug(f"Clearing widgets from GridLayout::{wid}")
        self.ids[wid].clear_widgets()

    def make_button(
        self,
        root_widget: str,
        id: str,
        text: str,
        markup: str,
        row: str,
        on_press: typing.Callable,
        on_release: typing.Callable,
    ):
        """Create buttons in a dynamic way"""
        self.debug(f"{id} -> {root_widget}")

        total = self.ids[root_widget].rows
        btn = Button(
            text=text,
            markup=markup,
            halign="center",
            font_size=Window.size[0] // 25,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn.id = id

        # define button methods to be callable in classes
        setattr(self, f"on_press_{id}", on_press)
        setattr(self, f"on_release_{id}", on_release)

        btn.bind(on_press=on_press)
        btn.bind(on_release=on_release)
        btn.x = 0
        btn.y = (Window.size[1] / total) * row
        btn.width = Window.size[0]
        btn.height = Window.size[1] / total

        self.ids[root_widget].add_widget(btn)
        self.ids[btn.id] = WeakProxy(btn)

        with self.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            Line(width=0.5, rectangle=(btn.x, btn.y, btn.width, btn.height))
