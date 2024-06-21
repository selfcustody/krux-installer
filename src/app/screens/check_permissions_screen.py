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
check_permissions_screen.py
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

if not sys.platform.startswith("win"):
    import distro
    import grp


class CheckPermissionsScreen(BaseScreen):
    """GreetingsScreen show Krux logo and check if user is in dialout group in linux"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="check_permissions_screen",
            name="CheckPermissionsScreen",
            **kwargs,
        )

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)
        self.bin = None
        self.bin_args = None
        self.group = None
        self.user = None
        self.in_dialout = False
        self.on_permission_created = None

        # START of on_press buttons
        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

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
                cmd = (
                    [self.bin] + [a for a in self.bin_args] + [self.group] + [self.user]
                )
                self.debug(f"cmd={cmd}")
                sudoer = SudoerLinux(name=f"Add {self.user} to {self.group}")
                sudoer.exec(cmd=cmd, env={}, callback=self.on_permission_created)
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

    def make_on_permissions_created(self) -> typing.Callable:
        """Create a callback to change"""

        def callback(output: str):
            self.debug(f"output={output}")
            logout_msg = self.translate("You may need to logout (or even reboot)")
            backin_msg = self.translate("and back in for the new group to take effect")
            not_worry_msg = self.translate(
                "Do not worry, this message won't appear again"
            )

            self.ids[f"{self.id}_button"].text = "\n".join(
                [
                    f"[size=32sp][color=#efcc00]{output}[/color][/size]",
                    "",
                    f"[size=16sp]{logout_msg}",
                    f"{backin_msg}.",
                    "",
                    f"{not_worry_msg}.[/size]",
                ]
            )
            self.bin = None
            self.bin_args = None
            self.group = None
            self.user = None

        return callback

    def update(self, *args, **kwargs):
        """
        In linux, will check for user permission on group
        dialout (debian-li ke) and uucp (archlinux-like) and
        add user to that group to allow sudoless flash
        """
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in ("ConfigKruxInstaller", "CheckPermissionsScreen"):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen: {name}")

        if key == "locale":
            self.locale = value

        elif key == "check_user":

            self.user = os.environ.get("USER")
            self.debug(f"Checking permissions for {self.user}")

            setup_msg = self.translate("Setup")
            for_msg = self.translate("for")

            self.ids[f"{self.id}_button"].text = (
                f"[size=32sp][color=#efcc00]{setup_msg} {self.user} {for_msg} {distro.name()}[/color][/size]"
            )

            if distro.id() == "debian" or distro.like() == "debian":
                self.bin = "/usr/bin/usermod"
                self.bin_arg = ["-a", "-G"]
                self.group = "dialout"

            elif distro.id() in ("arch", "manjaro"):
                self.bin = "/usr/bin/usermod"
                self.bin_args = ["-a", "-G"]
                self.group = "uucp"

            else:
                raise RuntimeError(f"Not implemented for '{distro.name(pretty=True)}'")

            fn = partial(self.update, name=self.name, key="check_group")
            Clock.schedule_once(fn, 2.1)

        elif key == "check_group":

            self.debug(f"Checking {self.group} permissions for {self.user}")
            check_msg = self.translate("Checking")
            perm_msg = self.translate("permissions for")

            self.ids[f"{self.id}_button"].text = (
                f"[size=32sp][color=#efcc00]{check_msg} {self.group} {perm_msg} {self.user}[/color][/size]"
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
                self.debug(f"Creating permission for {self.user}")
                warn_msg = self.translate("WARNING")
                first_msg = self.translate("This is the first run of KruxInstaller in")
                access_msg = self.translate(
                    "and it appears that you do not have privileged access to make flash procedures"
                )
                proceed_msg = self.translate(
                    "To proceed, click in the screen and a prompt will ask for your password"
                )
                exec_msg = self.translate("to execute the following command")

                self.ids[f"{self.id}_button"].text = "\n".join(
                    [
                        "[size=32sp][color=#efcc00]WARNING[/color][/size]",
                        "",
                        f'[size=16sp]{first_msg} "{distro.name(pretty=True)}"',
                        f"{access_msg}.",
                        proceed_msg,
                        f"{exec_msg}:",
                        ""
                        f"[color=#00ff00]{self.bin} {" ".join(self.bin_args)} {self.group} {self.user}[/color][/size]",
                    ]
                )
            else:
                self.set_screen(name="MainScreen", direction="left")

        else:
            raise ValueError(f"Invalid key: '{key}'")

    def on_enter(self):
        """
        check if user belongs to dialout|uucp group
        (groups that manage /tty/USB files)
        if belongs, add user to it
        """
        fn = partial(self.update, name=self.name, key="check_user")
        Clock.schedule_once(fn, 0)
