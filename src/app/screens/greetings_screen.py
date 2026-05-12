# The MIT License (MIT)

# Copyright (c) 2021-2026 Krux contributors

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
import sys
from functools import partial

from kivy.clock import Clock

from src.app.screens.base_screen import BaseScreen


class GreetingsScreen(BaseScreen):
    """GreetingsScreen show Krux logo"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="greetings_screen",
            name="GreetingsScreen",
            **kwargs,
        )

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1, resize_canvas=True)

        # Build logo
        self.make_image(
            wid=f"{self.id}_logo", root_widget=f"{self.id}_grid", source=self.logo_img
        )

    # pylint: disable=unused-argument
    def on_enter(self, *args):
        """
        When application start, after greeting user with the krux logo, it will need to check if
        user is running app in linux or non-linux. If running in linux, the user will be
        redirect to CheckPermissionsScreen and then to MainScreen. Win32 and Mac will be
        redirect to MainScreen.
        """
        fn_0 = partial(self.update, name=self.name, key="canvas")
        fn_1 = partial(self.update, name=self.name, key="check-permission")
        Clock.schedule_once(fn_0, 0)
        Clock.schedule_once(fn_1, 2.1)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """
        After show krux logo, verify:
        - in linux, if the current user is in dialout group to allow sudoless flash
        - then go directly to MainScreen
        """
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "check-permission":
                self.check_dialout_permission()

        setattr(GreetingsScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("KruxInstallerApp", self.name),
            on_update=getattr(GreetingsScreen, "on_update"),
        )

    def get_os_dialout_group(self):
        """Detect OS and properly return the 'dialout' group (in some distros can be 'uucp')"""
        detected = (None, None)
        try:
            with open("/etc/os-release", mode="r", encoding="utf-8") as f:
                os_info = f.readlines()

            os_data = {
                line.split("=")[0]: line.split("=")[1].strip().strip('"')
                for line in os_info
                if "=" in line
            }

            # Check for Debian-like systems (PopOS, Ubuntu, Linux Mint, etc.)
            if "ID_LIKE" in os_data and "debian" in os_data["ID_LIKE"]:
                detected = (
                    os_data["ID_LIKE"],
                    "dialout",
                )

            # Check for Red Hat-based systems (CentOS, Rocky Linux, etc.)
            if "ID_LIKE" in os_data and "rhel" in os_data["ID_LIKE"]:
                detected = (
                    os_data["ID_LIKE"],
                    "dialout",
                )

            # Check for SUSE-based systems (openSUSE, SUSE Linux Enterprise)
            if "ID_LIKE" in os_data and "suse" in os_data["ID_LIKE"]:
                detected = (
                    os_data["ID_LIKE"],
                    "dialout",
                )

            # Check for Fedora, to fix issue #115
            # see https://github.com/selfcustody/krux-installer/issues/115
            elif "ID" in os_data and "fedora" in os_data["ID"]:
                detected = (
                    os_data["ID"],
                    "dialout",
                )

            # Arch, Manjaro, Slackware, Gentoo
            if os_data.get("ID") in ("arch", "manjaro", "slackware", "gentoo"):
                detected = (os_data["ID"], "uucp")

            # For Alpine, Clear Linux, Solus, etc.
            if os_data.get("ID") in ("alpine", "clear-linux", "solus"):
                detected = (os_data["ID"], "dialout")

            # Check for NixOS 25.11 and allow it
            if os_data.get("ID") == "nixos":
                id_version = os_data.get("VERSION_ID", "unknown version")
                detected = (os_data["ID"], "dialout")
                print(f"Allowing NixOS {id_version} (experimental support)")

            if not detected[0]:
                exc = RuntimeError(
                    f"{os_data.get('PRETTY_NAME', 'Unknown Linux distribution')} not supported"
                )
                self.redirect_exception(exception=exc)

        except FileNotFoundError:
            exc = RuntimeError(
                "Unable to detect Linux distribution (no /etc/os-release found)."
            )
            self.redirect_exception(exception=exc)

        return detected

    def is_user_in_dialout_group(self, user: str, group: str):
        """Check if the provided user is in dialout"""
        _in_dialout = False

        try:
            import grp  # pylint: disable=import-outside-toplevel
        except ImportError:
            return _in_dialout

        for _grp in grp.getgrall():
            gr_name = _grp.gr_name
            if gr_name == group:
                for _grpuser in _grp.gr_mem:
                    if _grpuser == user:
                        self.info(f"'{user}' already in group '{gr_name}'")
                        _in_dialout = True

        return _in_dialout

    def check_dialout_permission(self):
        """
        Check dialout permission on Linux then proceed to MainScreen.
        On non-Linux systems, go directly to MainScreen.
        """
        if sys.platform.startswith("linux"):
            _user = str(os.environ.get("USER"))

            _distro, _group = self.get_os_dialout_group()

            if not self.is_user_in_dialout_group(user=_user, group=_group):
                ask = self.manager.get_screen("AskPermissionDialoutScreen")
                fns = [
                    partial(ask.update, name=self.name, key="user", value=_user),
                    partial(ask.update, name=self.name, key="group", value=_group),
                    partial(ask.update, name=self.name, key="distro", value=_distro),
                    partial(ask.update, name=self.name, key="screen"),
                ]

                for fn in fns:
                    Clock.schedule_once(fn, 0)

                self.set_screen(name="AskPermissionDialoutScreen", direction="left")
            else:
                self.set_screen(name="MainScreen", direction="left")

        else:
            self.set_screen(name="MainScreen", direction="left")
