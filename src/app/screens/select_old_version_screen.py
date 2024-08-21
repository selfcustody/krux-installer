#         The MIT License (MIT)

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
select_old_version_screen.py
"""
# pylint: disable=no-name-in-module
import re
import typing
from functools import partial
from kivy.clock import Clock
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from src.utils.selector import Selector
from .base_screen import BaseScreen


class SelectOldVersionScreen(BaseScreen):
    """SelectOldVersionScreen is where old versions can be selected"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_old_version_screen", name="SelectOldVersionScreen", **kwargs
        )

    def fetch_releases(self, old_versions: typing.List[str]):
        """Build a set of buttons to select version"""
        self.make_grid(wid="select_old_version_screen_grid", rows=len(old_versions) + 1)
        self.clear_grid(wid="select_old_version_screen_grid")

        for row, text in enumerate(old_versions):
            sanitized = (text.replace(".", "_").replace("/", "_"),)
            wid = f"select_old_version_{sanitized}"

            def _press(instance):
                self.debug(f"Calling {instance}::on_press")
                self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

            def _release(instance):
                self.debug(f"Calling {instance.id}::on_release")
                self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
                version = self.ids[instance.id].text
                self.debug(f"on_release::{instance.id} = {version}")
                main_screen = self.manager.get_screen("MainScreen")
                fn_version = partial(
                    main_screen.update, name=self.name, key="version", value=version
                )
                fn_device = partial(
                    main_screen.update,
                    name=self.name,
                    key="device",
                    value="select a new one",
                )
                Clock.schedule_once(fn_version, 0)
                Clock.schedule_once(fn_device, 0)
                self.set_screen(name="MainScreen", direction="right")

            self.make_button(
                row=row,
                id=wid,
                root_widget="select_old_version_screen_grid",
                text=f"[font=terminus]{text}[/font]",
                markup=True,
                on_press=_press,
                on_release=_release,
            )

        # Back Button
        def _press_back(instance):
            self.debug(f"Calling {instance}::on_press")
            self.set_background(
                wid="select_old_version_back", rgba=(0.25, 0.25, 0.25, 1)
            )

        def _release_back(instance):
            self.debug(f"Calling {instance}::on_release")
            self.set_background(wid="select_old_version_back", rgba=(0, 0, 0, 1))
            self.set_screen(name="SelectVersionScreen", direction="right")

        back = self.translate("Back")
        self.make_button(
            row=len(old_versions) + 1,
            id="select_old_version_back",
            root_widget="select_old_version_screen_grid",
            text=f"[font={SelectOldVersionScreen.get_font_name()}]{back}[/font]",
            markup=True,
            on_press=_press_back,
            on_release=_release_back,
        )

    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in ("ConfigKruxInstaller", "SelectOldVersionScreen"):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            if value is not None:
                self.locale = value

                if "select_old_version_back" in self.ids:
                    back = self.translate("Back")
                    self.ids["select_old_version_back"].text = "".join(
                        [
                            f"[font={SelectOldVersionScreen.get_font_name()}]",
                            back,
                            "[/font]",
                        ]
                    )

            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        else:
            self.redirect_error(msg=f'Invalid key: "{key}"')
