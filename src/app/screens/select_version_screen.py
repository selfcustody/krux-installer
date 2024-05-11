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
# pylint: disable=no-name-in-module
import re
from functools import partial
from kivy.clock import Clock
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from src.utils.selector import Selector
from .base_screen import BaseScreen


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
            ("select_version_old", "Old versions", False),
            ("select_version_back", "Back", False),
        ]

        # Push other releases to SelectOldVersionScreen

        select_old_version_screen = self.manager.get_screen("SelectOldVersionScreen")
        select_old_version_screen.fetch_releases(old_versions=selector.releases[1:-1])
        # START of buttons
        for row, _tuple in enumerate(buttons):

            # START of on_press buttons
            def _press(instance):
                self.debug(f"Calling Button::{instance.id}::on_press")
                if instance.id in (
                    "select_version_latest",
                    "select_version_beta",
                    "select_version_old",
                    "select_version_back",
                ):
                    self.set_background(wid=instance.id, rgba=(0.5, 0.5, 0.5, 0.5))
                else:
                    self.warning(f"Button::{instance.id} not found")

            # END of on_press buttons

            # START of on_release_buttons
            def _release(instance):
                self.debug(f"Calling Button::{instance.id}::on_release")
                if instance.id == "select_version_latest":
                    self.set_background(wid=instance.id, rgba=(0, 0, 0, 0))
                    version = self.ids[instance.id].text
                    self.debug(f"on_release::{instance.id} = {version}")
                    main_screen = self.manager.get_screen("MainScreen")
                    fn = partial(
                        main_screen.update, name=self.name, key="version", value=version
                    )
                    Clock.schedule_once(fn, 0)
                    self.set_screen(name="MainScreen", direction="right")
                if instance.id == "select_version_beta":
                    self.set_background(wid=instance.id, rgba=(0, 0, 0, 0))
                    version = self.ids[instance.id].text
                    self.debug(f"on_release::{instance.id} = {version}")

                    title = "[size=28sp][color=#efcc00][b]WARNING[/b][/color][/size]"
                    subtitle = "[size=18sp][color=#efcc00]This is our test (beta) repository[/color][/size]"
                    message = [
                        "These are unsigned binaries for the latest and most experimental features",
                        "and it's just for trying new things and providing feedback.",
                    ]

                    self.show_warning_beta(
                        title=title,
                        subtitle=subtitle,
                        message="\n".join(message),
                        version=version,
                    )
                elif instance.id == "select_version_old":
                    self.set_background(wid="select_version_old", rgba=(0, 0, 0, 0))
                    self.set_screen(name="SelectOldVersionScreen", direction="left")
                elif instance.id == "select_version_back":
                    self.set_background(wid="select_version_back", rgba=(0, 0, 0, 0))
                    self.set_screen(name="MainScreen", direction="right")
                else:
                    self.warning(f"Button::{instance.id} not found")

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

    def show_warning_beta(self, title: str, subtitle: str, message: str, version: str):
        # Create widgets
        view = ModalView(size_hint=(1, 1), background_color=(0, 0, 0))
        _title = Label(text=title, markup=True, halign="center")
        _subtitle = Label(text=subtitle, markup=True, halign="center")
        _message = Label(text=message, halign="center")
        ok = Button(text="I understand")
        box = BoxLayout(orientation="vertical", spacing=2)

        ok.id = "select_version_warning_ok"

        # Structure them
        box.add_widget(_title)
        box.add_widget(_subtitle)
        box.add_widget(_message)
        box.add_widget(ok)
        view.add_widget(box)

        # define events
        def on_ok(instance):
            self.debug(f"Button 'I understand' pressed")
            main_screen = self.manager.get_screen("MainScreen")
            fn = partial(
                main_screen.update, name=self.name, key="version", value=version
            )
            Clock.schedule_once(fn, 0)
            self.set_screen(name="MainScreen", direction="right")
            return False

        ok.bind(on_press=view.dismiss)
        view.bind(on_dismiss=on_ok)

        # show it
        view.open()
