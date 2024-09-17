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
select_version_screen.py
"""
# pylint: disable=no-name-in-module
from functools import partial
from kivy.clock import Clock
from src.utils.selector import Selector
from src.app.screens.base_screen import BaseScreen


class SelectVersionScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_version_screen", name="SelectVersionScreen", **kwargs
        )

        # Build grid where buttons will be placed
        self.make_grid(wid="select_version_screen_grid", rows=4)

    def clear(self):
        """Clear the list of children widgets buttons"""
        self.ids["select_version_screen_grid"].clear_widgets()

    def build_select_version_latest_button(self, text: str):
        """Make a button to select latest version and a staticmethod that call instance variables"""

        def on_press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            version = self.ids[instance.id].text
            self.debug(f"on_release::{instance.id} = {version}")
            main_screen = self.manager.get_screen("MainScreen")
            fn_version = partial(
                main_screen.update,
                name=self.name,
                key="version",
                value=version,
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

        wid = f"{self.id}_latest"

        self.make_button(
            row=0,
            wid=wid,
            root_widget="select_version_screen_grid",
            text=text,
            font_factor=28,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def build_select_beta_version_button(self, text: str):
        """Make a button to select beta version and a staticmethod that call instance variables"""

        def on_press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            version = self.ids[instance.id].text
            main_screen = self.manager.get_screen("MainScreen")
            fn_version = partial(
                main_screen.update,
                name=self.name,
                key="version",
                value="odudex/krux_binaries",
            )
            fn_device = partial(
                main_screen.update,
                name=self.name,
                key="device",
                value="select a new one",
            )
            Clock.schedule_once(fn_version, 0)
            Clock.schedule_once(fn_device, 0)
            self.debug(f"on_release::{instance.id} = {version}")
            self.set_screen(name="WarningBetaScreen", direction="left")

        wid = f"{self.id}_beta"
        self.make_button(
            row=1,
            wid=wid,
            root_widget="select_version_screen_grid",
            text=text,
            font_factor=28,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def build_select_version_old_button(self, text: str):
        """Make a button to select old versions and a staticmethod that call instance variables"""

        def on_press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            self.set_screen(name="SelectOldVersionScreen", direction="left")

        wid = f"{self.id}_old"
        self.make_button(
            row=2,
            wid=wid,
            root_widget="select_version_screen_grid",
            text=text,
            font_factor=28,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def build_select_version_back_button(self, text: str):
        """Make a button to back and a staticmethod that call instance variables"""

        def on_press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            self.set_screen(name="MainScreen", direction="right")

        wid = f"{self.id}_back"
        self.make_button(
            row=3,
            wid=wid,
            root_widget="select_version_screen_grid",
            text=text,
            font_factor=28,
            halign=None,
            on_press=on_press,
            on_release=on_release,
            on_ref_press=None,
        )

    def fetch_releases(self):
        """Build a set of buttons to select version"""
        try:
            self.clear()
            selector = Selector()
            self.build_select_version_latest_button(selector.releases[0])
            self.build_select_beta_version_button(selector.releases[-1])
            self.build_select_version_old_button(self.translate("Old versions"))
            self.build_select_version_back_button(self.translate("Back"))

            # Push other releases to SelectOldVersionScreen
            select_old_version_screen = self.manager.get_screen(
                "SelectOldVersionScreen"
            )
            select_old_version_screen.fetch_releases(
                old_versions=selector.releases[1:-1]
            )

        # pylint: disable=broad-exception-caught
        except Exception as exc:
            self.error(str(exc))
            self.redirect_exception(exception=exc)

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
            allowed_screens=("ConfigKruxInstaller", "SelectVersionScreen"),
            on_update=None,
        )
