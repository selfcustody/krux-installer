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
select_old_version_screen.py
"""
# pylint: disable=no-name-in-module
import typing
from functools import partial
from kivy.clock import Clock
from .base_screen import BaseScreen


class SelectOldVersionScreen(BaseScreen):
    """SelectOldVersionScreen is where old versions can be selected"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_old_version_screen", name="SelectOldVersionScreen", **kwargs
        )

    def build_version_button(self, text: str, row: int):
        """Dynamically build a button to set a firmware version"""
        sanitized = (text.replace(".", "_").replace("/", "_"),)
        wid = f"select_old_version_{sanitized}"

        def on_press(instance):
            self.debug(f"Calling {instance}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release(instance):
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
            wid=wid,
            root_widget="select_old_version_screen_grid",
            text=text,
            font_factor=28,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def build_back_button(self, text: str, row: int):
        """Build a button to sback to main screen"""

        # Back Button
        def on_press(instance):
            self.debug(f"Calling {instance}::on_press")
            self.set_background(
                wid="select_old_version_back", rgba=(0.25, 0.25, 0.25, 1)
            )

        def on_release(instance):
            self.debug(f"Calling {instance}::on_release")
            self.set_background(wid="select_old_version_back", rgba=(0, 0, 0, 1))
            self.set_screen(name="SelectVersionScreen", direction="right")

        self.make_button(
            row=row,
            wid="select_old_version_back",
            root_widget="select_old_version_screen_grid",
            text=text,
            font_factor=28,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def fetch_releases(self, old_versions: typing.List[str]):
        """Build a set of buttons to select version"""
        self.make_grid(wid="select_old_version_screen_grid", rows=len(old_versions) + 1)
        self.clear_grid(wid="select_old_version_screen_grid")

        for row, text in enumerate(old_versions):
            self.build_version_button(text, row)

        back = self.translate("Back")
        self.build_back_button(back, len(old_versions) + 1)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("ConfigKruxInstaller", "SelectOldVersionScreen"),
            on_update=None,
        )
