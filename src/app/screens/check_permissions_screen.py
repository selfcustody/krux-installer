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
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.core.window import Window
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

        # These variables will setup the inclusion
        # in dialout group, if necessary
        self.bin = None
        self.bin_args = None
        self.group = None
        self.user = None
        self.in_dialout = False
        self.on_permission_created = None

        def _on_ref_press(*args):
            print(args)
            if args[1] == "Allow":
                # If user isnt in the dialout group,
                # but the configuration was done correctly
                # create the command

                if self.on_permission_created and self.bin_args:
                    try:
                        cmd = (
                            [self.bin]
                            + [a for a in self.bin_args]
                            + [self.group]
                            + [self.user]
                        )
                        self.debug(f"cmd={cmd}")
                        sudoer = SudoerLinux(name=f"Add {self.user} to {self.group}")
                        sudoer.exec(
                            cmd=cmd, env={}, callback=self.on_permission_created
                        )
                    except Exception as err:
                        self.redirect_error(msg=str(err.__traceback__))
                else:
                    self.redirect_error(
                        msg=f"Invalid on_permission_created: {self.on_permission_created}"
                    )

            if args[1] == "Deny":
                App.get_running_app().stop()

        self.make_label(
            wid=f"{self.id}_label",
            text="",
            root_widget=f"{self.id}_grid",
            markup=True,
            halign="justify",
        )

        setattr(CheckPermissionsScreen, f"on_ref_press_{self.id}_label", _on_ref_press)
        self.ids[f"{self.id}_label"].bind(on_ref_press=_on_ref_press)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def update(self, *args, **kwargs):
        """
        In linux, will check for user permission on group
        dialout (debian-li ke) and uucp (archlinux-like) and
        add user to that group to allow sudoless flash
        """
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "CheckPermissionsScreen",
            "CheckPermissionsScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(msg=f"Invalid screen: '{name}'")
            return

        if key == "locale":
            if value is None or value.strip() == "":
                self.redirect_error(msg=f"Invalid locale: '{value}'")
            else:
                self.locale = value

        elif key == "canvas":
            # prepare background
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        elif key == "check_user":

            # Here's where the check process start
            # first get the current user, then verify
            # the linux distribution used and use the
            # proper command to add the user in 'dialout' (
            # group (in some distros, can be 'uucp')
            self.user = os.environ.get("USER")
            self.debug(f"Checking permissions for {self.user}")

            setup_msg = self.translate("Setup")
            for_msg = self.translate("for")

            self.ids[f"{self.id}_label"].text = "".join(
                [
                    f"[font={CheckPermissionsScreen.get_font_name()}]",
                    f"[size={self.SIZE_MM}sp]",
                    f"[color=#efcc00]{setup_msg} {self.user} {for_msg} {distro.name()}[/color]",
                    "[/size]",
                    "[/font]",
                ]
            )

            if distro.id() in ("ubuntu", "fedora", "linuxmint"):
                self.bin = "/usr/bin/usermod"
                self.bin_arg = ["-a", "-G"]
                self.group = "dialout"

            elif distro.id() in ("arch", "manjaro", "slackware", "gentoo"):
                self.bin = "/usr/bin/usermod"
                self.bin_args = ["-a", "-G"]
                self.group = "uucp"

            elif distro.like() == "debian":
                self.bin = "/usr/bin/usermod"
                self.bin_args = ["-a", "-G"]
                self.group = "dialout"

            else:
                self.redirect_error(
                    msg=f"Not implemented for '{distro.name(pretty=True)}'"
                )
                return

            fn = partial(self.update, name=self.name, key="check_group")
            Clock.schedule_once(fn, 2.1)

        elif key == "check_group":

            # Here is where we check if the user belongs to group
            # 'dialout' (in some distros, will be 'uucp')
            self.debug(f"Checking {self.group} permissions for {self.user}")
            check_msg = self.translate("Checking")
            perm_msg = self.translate("permissions for")

            self.ids[f"{self.id}_label"].text = "".join(
                [
                    f"[font={CheckPermissionsScreen.get_font_name()}]",
                    f"[size={self.SIZE_G}sp]",
                    f"[color=#efcc00]{check_msg} {self.group} {perm_msg} {self.user}[/color][/size]",
                    "[/font]",
                ]
            )

            # loop throug all groups and check
            for group in grp.getgrall():
                if self.group == group.gr_name:
                    self.debug(f"Found {group.gr_name}")
                    for user in group[3]:
                        if user == self.user:
                            self.debug(f"'{self.user}' already in group '{self.group}'")
                            self.in_dialout = True

            self.debug(f"in_dialout={self.in_dialout}")

            # if not in group, warn user
            # and then ask for click in screen
            # to proceed with the operation
            if not self.in_dialout:
                self.debug(f"Creating permission for {self.user}")
                warn_msg = self.translate("WARNING")
                first_msg = self.translate("This is the first run of KruxInstaller in")
                access_msg = self.translate(
                    "and it appears that you do not have privileged access to make flash procedures"
                )
                proceed_msg = self.translate(
                    "To proceed, click in the Allow button and a prompt will ask for your password"
                )
                exec_msg = self.translate("to execute the following command")

                self.ids[f"{self.id}_label"].text = "\n".join(
                    [
                        f"[font={CheckPermissionsScreen.get_font_name()}]"
                        f"[size={self.SIZE_G}sp][color=#efcc00]{warn_msg}[/color][/size]",
                        "",
                        f'[size={self.SIZE_MP}sp]{first_msg} "{distro.name(pretty=True)}"',
                        f"{access_msg}.",
                        proceed_msg,
                        f"{exec_msg}:",
                        "[/font]" "",
                        "",
                        "[font=terminus]" "[color=#00ff00]",
                        f"{self.bin} {" ".join(self.bin_args or [])} {self.group} {self.user}",
                        "[/color]",
                        "[/size]",
                        "[/font]",
                        "",
                        "",
                        f"[font={CheckPermissionsScreen.get_font_name()}]",
                        f"[size={self.SIZE_M}]",
                        "        ".join(
                            [
                                "[color=#00FF00][ref=Allow]Allow[/ref][/color]",
                                "[color=#FF0000][ref=Deny]Deny[/ref][/color]",
                            ]
                        ),
                        "[/size]",
                        "[/font]",
                    ]
                )

                # Check if callback is created and create if isnt exist
                # (in tests you can mock it and the conditional below will not be called)
                if self.on_permission_created is None:
                    fn = partial(
                        self.update, name=self.name, key="make_on_permission_created"
                    )
                    Clock.schedule_once(fn, 2.1)

            else:
                self.set_screen(name="CheckInternetConnectionScreen", direction="left")

        elif key == "make_on_permission_created":

            # When user is added to dialout group
            # ask for user to reboot to apply the changes
            # and the ability to flash take place
            def on_permission_created(output: str):
                self.debug(f"output={output}")
                logout_msg = self.translate("You may need to logout (or even reboot)")
                backin_msg = self.translate(
                    "and back in for the new group to take effect"
                )
                not_worry_msg = self.translate(
                    "Do not worry, this message won't appear again"
                )

                self.ids[f"{self.id}_label"].text = "\n".join(
                    [
                        f"[font={CheckPermissionsScreen.get_font_name()}]",
                        f"[size={self.SIZE_M}sp][color=#efcc00]{output}[/color][/size]",
                        "",
                        f"[size={self.SIZE_M}sp]{logout_msg}",
                        f"{backin_msg}.",
                        "",
                        f"{not_worry_msg}.[/size]",
                        "[/font]",
                    ]
                )

                self.bin = None
                self.bin_args = None
                self.group = None
                self.user = None

            setattr(self, "on_permission_created", on_permission_created)

        else:
            self.redirect_error(msg=f"Invalid key: '{key}'")

    def on_enter(self):
        """
        check if user belongs to dialout|uucp group
        (groups that manage /tty/USB files)
        if belongs, add user to it
        """
        fn = partial(self.update, name=self.name, key="check_user")
        Clock.schedule_once(fn, 0)
