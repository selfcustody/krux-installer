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
import os
import re
import sys
import typing
from pathlib import Path
from functools import partial
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.weakproxy import WeakProxy
from src.i18n import T
from src.utils.trigger import Trigger


class BaseScreen(Screen, Trigger):
    """Main screen is the 'Home' page"""

    def __init__(self, wid: str, name: str, **kwargs):
        super().__init__(**kwargs)
        self.id = wid
        self.name = name

        # Check if this is a Pyinstaller bundle
        # and set the correct path to find some assets
        if getattr(sys, "frozen", False):
            root_assets_path = getattr(sys, "_MEIPASS")
        else:
            root_assets_path = Path(__file__).parent.parent.parent.parent

        self._logo_img = os.path.join(root_assets_path, "assets", "logo.png")
        self._warn_img = os.path.join(root_assets_path, "assets", "warning.png")
        self._load_img = os.path.join(root_assets_path, "assets", "load.gif")
        self._done_img = os.path.join(root_assets_path, "assets", "done.png")

        self.locale = BaseScreen.get_locale()

        # Setup the correct font size
        if sys.platform in ("linux", "win32"):
            self.SIZE_XG = Window.size[0] // 4
            self.SIZE_GG = Window.size[0] // 8
            self.SIZE_G = Window.size[0] // 16
            self.SIZE_MM = Window.size[0] // 24
            self.SIZE_M = Window.size[0] // 32
            self.SIZE_MP = Window.size[0] // 48
            self.SIZE_P = Window.size[0] // 64
            self.SIZE_PP = Window.size[0] // 128

        elif sys.platform == "darwin":
            self.SIZE_XG = Window.size[0] // 16
            self.SIZE_GG = Window.size[0] // 24
            self.SIZE_G = Window.size[0] // 32
            self.SIZE_MM = Window.size[0] // 48
            self.SIZE_M = Window.size[0] // 64
            self.SIZE_MP = Window.size[0] // 128
            self.SIZE_P = Window.size[0] // 192
            self.SIZE_PP = Window.size[0] // 256

    @property
    def logo_img(self) -> str:
        """Getter for logo_img"""
        self.debug(f"getter::logo_img={self._logo_img}")
        return self._logo_img

    @property
    def warn_img(self) -> str:
        """Getter for warn_img"""
        self.debug(f"getter::warn_img={self._warn_img}")
        return self._warn_img

    @property
    def load_img(self) -> str:
        """Getter for load_img"""
        self.debug(f"getter::load_img={self._load_img}")
        return self._load_img

    @property
    def done_img(self) -> str:
        """Getter for done_img"""
        self.debug(f"getter::done_img={self._done_img}")
        return self._done_img

    @property
    def locale(self) -> str:
        """Getter for locale property"""
        return self._locale

    @locale.setter
    def locale(self, value: str):
        """Setter for locale property"""
        self.debug(f"locale = {value}")
        self._locale = value

    def translate(self, key: str) -> str:
        """Translate some message as key"""
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
        if wid not in self.ids:
            self.debug(f"Building GridLayout::{wid}")
            grid = GridLayout(cols=1, rows=rows)
            grid.id = wid
            self.add_widget(grid)
            self.ids[wid] = WeakProxy(grid)
        else:
            self.debug(f"GridLayout::{wid} already exist")

    def make_subgrid(self, wid: str, rows: int, root_widget: str):
        """Build grid where buttons will be placed"""
        self.debug(f"Building GridLayout::{wid}")
        grid = GridLayout(cols=1, rows=rows)
        grid.id = wid
        self.ids[root_widget].add_widget(grid)
        self.ids[wid] = WeakProxy(grid)

    def make_label(self, wid: str, text: str, root_widget: str, halign: str):
        """Build grid where buttons will be placed"""
        self.debug(f"Building GridLayout::{wid}")
        label = Label(text=text, markup=True, halign=halign)
        label.id = wid
        self.ids[root_widget].add_widget(label)
        self.ids[wid] = WeakProxy(label)

    def make_image(self, wid: str, source: str, root_widget: str):
        """Build grid where buttons will be placed"""
        self.debug(f"Building Image::{wid}")
        image = Image(source=source, fit_mode="scale-down")
        image.id = wid
        self.ids[root_widget].add_widget(image)
        self.ids[wid] = WeakProxy(image)

    def clear_grid(self, wid: str):
        """Clear GridLayout widget"""
        self.debug(f"Clearing widgets from GridLayout::{wid}")
        self.ids[wid].clear_widgets()

    def make_button(
        self,
        root_widget: str,
        wid: str,
        text: str,
        row: int,
        on_press: typing.Callable,
        on_release: typing.Callable,
    ):
        """Create buttons in a dynamic way"""
        self.debug(f"{wid} -> {root_widget}")

        total = self.ids[root_widget].rows
        btn = Button(
            text=text,
            markup=True,
            halign="center",
            font_size=Window.size[0] // 25,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
        )
        btn.id = wid

        # define button methods to be callable in classes
        setattr(self, f"on_press_{wid}", on_press)
        setattr(self, f"on_release_{wid}", on_release)

        btn.bind(on_press=on_press)
        btn.bind(on_release=on_release)
        btn.x = 0
        btn.y = (Window.size[1] / total) * row
        btn.width = Window.size[0]
        btn.height = Window.size[1] / total
        self.ids[root_widget].add_widget(btn)
        self.ids[btn.id] = WeakProxy(btn)

        self.debug(
            f"button::{id} row={row}, pos_hint={btn.pos_hint}, size_hint={btn.size_hint}"
        )

    def redirect_exception(self, exception: Exception):
        """Get an exception and prepare a ErrorScreen rendering"""
        screen = self.manager.get_screen("ErrorScreen")
        fns = [
            partial(screen.update, name=self.name, key="canvas"),
            partial(screen.update, name=self.name, key="error", value=exception),
        ]

        for fn in fns:
            Clock.schedule_once(fn, 0)

        self.set_screen(name="ErrorScreen", direction="left")

    def update_screen(
        self,
        name: str,
        key: str,
        value: typing.Any,
        allowed_screens: typing.Tuple,
        on_update: typing.Callable | None,
    ):
        """
        Update a screen in accord with the valid ones, here or in on_update callback
        """
        if name in allowed_screens:
            self.debug(f"Updating {self.name} from {name}...")
        else:
            exc = RuntimeError(f"Invalid screen name: {name}")
            self.redirect_exception(exception=exc)
            return

        if key == "locale":
            if value is not None:
                self.locale = value
            else:
                exc = RuntimeError(f"Invalid value for key '{key}': '{value}'")
                self.redirect_exception(exception=exc)

        if key == "canvas":
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        if on_update is not None:
            on_update()

    @staticmethod
    def quit_app():
        """Stop the kivy process"""
        app = App.get_running_app()
        app.stop()

    @staticmethod
    def get_destdir_assets() -> str:
        """Return the current selected path of destination assets directory"""
        app = App.get_running_app()
        return app.config.get("destdir", "assets")

    @staticmethod
    def get_baudrate() -> int:
        """Return the current selected baudrate"""
        app = App.get_running_app()
        return int(app.config.get("flash", "baudrate"))

    @staticmethod
    def get_locale() -> str:
        """Return the current locale"""
        app = App.get_running_app()
        locale = app.config.get("locale", "lang")

        if sys.platform in ("linux", "darwin"):
            locale = locale.split(".")
            return f"{locale[0].replace("-", "_")}.{locale[1]}"

        if sys.platform == "win32":
            return f"{locale}.UTF-8"

        raise RuntimeError(f"Not implemented for '{sys.platform}'")

    @staticmethod
    def open_settings():
        """Open the Settings screen"""
        app = App.get_running_app()
        app.open_settings()

    @staticmethod
    def sanitize_markup(msg: str) -> str:
        """
        Sanitize a message that come with [ ]
        and clean it (used in FlashScreen and WipeScreen)
        """
        cleanr = re.compile("\\[.*?\\]")
        return re.sub(cleanr, "", msg)
