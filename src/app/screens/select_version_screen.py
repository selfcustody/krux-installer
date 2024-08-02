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
import re
from functools import partial
from kivy.clock import Clock
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Line
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

    def fetch_releases(self):
        """Build a set of buttons to select version"""
        selector = Selector()

        buttons = [
            ("select_version_latest", selector.releases[0], False),
            ("select_version_beta", selector.releases[-1], False),
            ("select_version_old", self.translate("Old versions"), False),
            ("select_version_back", self.translate("Back"), False),
        ]

        # Push other releases to SelectOldVersionScreen

        select_old_version_screen = self.manager.get_screen("SelectOldVersionScreen")
        select_old_version_screen.fetch_releases(old_versions=selector.releases[1:-1])
        # START of buttons
        for row, _tuple in enumerate(buttons):

            # START of on_press buttons
            def _press(instance):
                self.debug(f"Calling Button::{instance.id}::on_press")
                self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

            # START of on_release_buttons
            def _release(instance):
                self.debug(f"Calling Button::{instance.id}::on_release")
                self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))

                if instance.id == "select_version_latest":
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

                if instance.id == "select_version_beta":
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

                if instance.id == "select_version_old":
                    self.set_screen(name="SelectOldVersionScreen", direction="left")

                if instance.id == "select_version_back":
                    self.set_screen(name="MainScreen", direction="right")

            # END of on_release buttons

            self.make_button(
                row=row,
                id=_tuple[0],
                root_widget="select_version_screen_grid",
                text=_tuple[1],
                markup=_tuple[2],
                on_press=_press,
                on_release=_release,
            )

    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in ("ConfigKruxInstaller", "SelectVersionScreen"):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            if value is not None:
                self.locale = value
                if "select_version_old" in self.ids:
                    self.ids["select_version_old"].text = self.translate("Old versions")

                if "select_version_back" in self.ids:
                    self.ids["select_version_back"].text = self.translate("Back")

            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        else:
            self.redirect_error(f'Invalid key: "{key}"')
