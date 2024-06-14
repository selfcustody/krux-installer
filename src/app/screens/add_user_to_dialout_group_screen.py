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
add_user_to_dialout_group_screen.py
"""
import os
import re
import typing
import sys
import distro
from functools import partial
from kivy.clock import Clock
from kivy.app import App
from kivy.cache import Cache
from .base_screen import BaseScreen
from src.i18n import T
from pysudoer import SudoerLinux


class AddUserToDialoutGroupScreen(BaseScreen):
    """AddUserToDialoutGroupScreen add user to dialout group screen in linux"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="add_user_to_dialout_screen",
            name="AddUserToDialoutGroupScreen",
            **kwargs,
        )

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)

        # START of on_press buttons
        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_permission_created(output: str):
            self.debug(f"output={output}")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 0))
            self.set_screen(name="MainScreen", direction="right")

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            user = os.environ.get("USER")

            if distro.id() == "debian" or distro.like() == "debian":
                bin = "/usr/bin/adduser"
                bin_arg = "-aG"
                group = "dialout"

            elif distro.id() == "arch" or distro.id() == "manjaro":
                bin = "/usr/bin/useradd"
                bin_arg = "-g"
                group = "uucp"

            else:
                raise RuntimeError(f"Not implemented for '{distro.name(pretty=True)}'")

            cmd = [bin, bin_arg, user, group]
            self.debug(f"cmd={cmd}")
            sudoer = SudoerLinux(name=f"Add {user} to {group}")
            sudoer.exec(cmd=cmd, env={}, callback=on_permission_created)

        self.make_button(
            row=0,
            id=f"{self.id}_button",
            root_widget=f"{self.id}_grid",
            text="\n".join(
                [
                    "We will ask for your permission allow us",
                    "to access the group responsible",
                    "for allowing you to flash krux in your device",
                ]
            ),
            markup=True,
            on_press=_press,
            on_release=_release,
        )
