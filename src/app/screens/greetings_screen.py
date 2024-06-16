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
greetings_screen.py
"""
import os
import re
import typing
import sys
import time
from functools import partial
from kivy.clock import Clock
from kivy.app import App
from kivy.cache import Cache
from .base_screen import BaseScreen
from src.i18n import T
from pysudoer import SudoerLinux


class GreetingsScreen(BaseScreen):
    """GreetingsScreen show Krux logo and check if user is in dialout group in linux"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="greetings_screen",
            name="GreetingsScreen",
            **kwargs,
        )

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)
        self.bin = None
        self.bin_args = None
        self.group = None
        self.user = None
        self.in_dialout = False

        # START of on_press buttons
        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        def on_permission_created(output: str):
            self.debug(f"output={output}")
            self.ids[f"{self.id}_button"].text = "\n".join(
                [
                    f"[size=32sp][color=#efcc00]{output}[/color][/size]",
                    "",
                    f"[size=16sp]You may need to logout (or even reboot)",
                    "and back in for the new group to take effect." "",
                    "Do not worry, this message won't appear again.",
                ]
            )
            self.bin = None
            self.bin_args = None
            self.group = None
            self.user = None

        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=f"{instance.id}", rgba=(0, 0, 0, 1))
            if (
                sys.platform == "linux"
                and self.bin
                and self.bin_args
                and self.group
                and self.user
            ):
                cmd = [self.bin]
                for a in self.bin_args:
                    cmd.append(a)
                cmd.append(self.group)
                cmd.append(self.user)

                self.debug(f"cmd={cmd}")
                sudoer = SudoerLinux(name=f"Add {self.user} to {self.group}")
                sudoer.exec(cmd=cmd, env={}, callback=on_permission_created)
            else:
                self.set_screen(name="MainScreen", direction="left")

        self.make_button(
            row=0,
            id=f"{self.id}_button",
            root_widget=f"{self.id}_grid",
            text="",
            markup=True,
            on_press=_press,
            on_release=_release,
        )

        self.ids[f"{self.id}_button"].text = "\n".join(
            [
                "     ██           ",
                "     ██           ",
                "     ██           ",
                "   ██████         ",
                "     ██           ",
                "       ██   ██       ",
                "       ██  ██        ",
                "      ████         ",
                "       ██  ██        ",
                "       ██   ██       ",
                "       ██    ██      ",
                "                    ",
                "   KRUX INSTALLER   ",
            ]
        )

    def update(self, *args, **kwargs):
        """
        In linux, will check for user permission on group
        dialout (debian-like) and uucp (archlinux-like) and
        add user to that group to allow sudoless flash
        """
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in ("ConfigKruxInstaller", "GreetingsScreen"):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen: {name}")

        if key == "check_user":
            import distro

            self.user = os.environ.get("USER")
            self.debug(f"Checking permissions for {self.user}")
            self.ids[f"{self.id}_button"].text = (
                f"[size=32sp][color=#efcc00]Setup {self.user} for {distro.name()}[/color][/size]"
            )

            if distro.id() == "debian" or distro.like() == "debian":
                self.bin = "/usr/bin/usermod"
                self.bin_arg = ["-a", "-G"]
                self.group = "dialout"

            elif distro.id() == "arch" or distro.id() == "manjaro":
                self.bin = "/usr/bin/usermod"
                self.bin_args = ["-a", "-G"]
                self.group = "uucp"

            else:
                raise RuntimeError(f"Not implemented for '{distro.name(pretty=True)}'")

            fn = partial(self.update, name=self.name, key="check_group")
            Clock.schedule_once(fn, 2)

        elif key == "check_group":
            import grp

            self.debug(f"Checking%s {self.group} permissions for {self.user}")
            self.ids[f"{self.id}_button"].text = (
                f"[size=32sp][color=#efcc00]Checking {self.group} permissions for {self.user}[/color][/size]"
            )

            for group in grp.getgrall():
                if self.group == group.gr_name:
                    self.debug(f"Found {group.gr_name}")
                    for user in group[3]:
                        if user == self.user:
                            self.debug(f"'{self.user}' already in group '{self.group}'")
                            self.in_dialout = True

            self.debug(f"in_dialout={self.in_dialout}")
            if not self.in_dialout:
                fn = partial(self.update, name=self.name, key="show_permission_message")
            else:
                fn = partial(self.update, name=self.name, key="skip_permission_message")

            Clock.schedule_once(fn, 2)

        elif key == "show_permission_message":
            import distro

            if not self.in_dialout:
                self.debug(f"Creating permission for {self.user}")
                self.ids[f"{self.id}_button"].text = "\n".join(
                    [
                        "[size=32sp][color=#efcc00]WARNING[/color][/size]",
                        "",
                        f'[size=16sp]This is first run of KruxInstaller in "{distro.name(pretty=True)}"',
                        f'and and it appears that you, the user "{self.user}",',
                        f'isn\'t within the "{self.group}" group, which enables the execution of',
                        "privileged procedures on USB devices (in this case, the firmware flash)",
                        "",
                        "To proceed, click in the screen and a prompt will ask for your password",
                        "to execute the following command:" "",
                        ""
                        f"[color=#00ff00]{self.bin} {" ".join(self.bin_args)} {self.group} {self.user}[/color][/size]",
                    ]
                )

        elif key == "skip_permission_message":
            if self.in_dialout:
                self.debug(f"{self.user} permissioned")
                self.set_screen(name="MainScreen", direction="left")

        elif key == "change_screen":
            self.set_screen(name=value, direction="left")

        else:
            raise ValueError(f"Invalid key: '{key}'")

    def on_enter(self):
        """
        check if user belongs to dialout|uucp group
        (groups that manage /tty/USB files)
        if belongs, add user to it
        """
        if sys.platform == "linux":
            fn = partial(self.update, name=self.name, key="check_user")

        else:
            fn = partial(self.update, name=self.name, key="skip_permission_message")

        Clock.schedule_once(fn, 0)
