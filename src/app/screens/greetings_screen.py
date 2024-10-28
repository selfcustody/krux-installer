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
import sys
from functools import partial
from kivy.clock import Clock
from src.utils.selector import Selector
from src.app.screens.base_screen import BaseScreen

if sys.platform.startswith("linux"):
    import grp  # pylint: disable=import-error


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
        - check the internet connection
            - if have, update the firmware version to the latest
        """
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "check-permission":
                self.check_dialout_permission()

            if key == "check-internet-connection":
                self.check_internet_connection()

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
                )  # Pop!_OS will fall under this

            # Check for Red Hat-based systems (Fedora, CentOS, Rocky Linux, etc.)
            if "ID_LIKE" in os_data and "rhel" in os_data["ID_LIKE"]:
                detected = (
                    os_data["ID_LIKE"],
                    "dialout",
                )  # Red Hat-based systems often use `dialout`

            # Check for SUSE-based systems (openSUSE, SUSE Linux Enterprise)
            if "ID_LIKE" in os_data and "suse" in os_data["ID_LIKE"]:
                detected = (
                    os_data["ID_LIKE"],
                    "dialout",
                )  # SUSE systems also often use `dialout`

            # Arch, Manjaro, Slackware, Gentoo
            if os_data.get("ID") in ("arch", "manjaro", "slackware", "gentoo"):
                detected = (os_data["ID"], "uucp")

            # For Alpine, Clear Linux, Solus, etc.
            if os_data.get("ID") in ("alpine", "clear-linux", "solus"):
                detected = (os_data["ID"], "dialout")

            if not detected[0]:
                # If none of the conditions match, fall back to the default group
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

        # loop throug all linux groups and check
        # if the user is registered in the "dialout" group
        # pylint: disable=possibly-used-before-assignment
        for _grp in grp.getgrall():
            gr_name = _grp.gr_name
            if gr_name == group:
                # for _grpuser in _grp[3]:
                for _grpuser in _grp.gr_mem:
                    if _grpuser == user:
                        self.info(f"'{user}' already in group '{gr_name}'")
                        _in_dialout = True

        return _in_dialout

    def check_dialout_permission(self):
        """
        Here's where the check process start
        first get the current user, then verify
        the linux distribution used and use the
        proper command to add the user in 'dialout'
        group (in some distros, can be 'uucp')
        """
        if sys.platform.startswith("linux"):
            # get current user
            _user = str(os.environ.get("USER"))
            _in_dialout = False

            # Set default group in case no match is found
            _distro, _group = self.get_os_dialout_group()

            # if user is not in dialout group, warn user
            # and then redirect to a screen that will
            # proceed with the proper operation
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
                fn = partial(
                    self.update, name=self.name, key="check-internet-connection"
                )
                Clock.schedule_once(fn, 0)

        else:
            fn = partial(self.update, name=self.name, key="check-internet-connection")
            Clock.schedule_once(fn, 0)

    def check_internet_connection(self):
        """
        In reality, this method get the latest version and set to
        select version button on main_screen. But it can work as
        internet connection check
        """
        try:
            selector = Selector()
            main_screen = self.manager.get_screen("MainScreen")
            fn = partial(
                main_screen.update,
                name=self.name,
                key="version",
                value=selector.releases[0],
            )
            Clock.schedule_once(fn, 0)
            self.set_screen(name="MainScreen", direction="left")

        # pylint: disable=broad-exception-caught
        except Exception as exc:
            self.error(str(exc))
            self.redirect_exception(exception=exc)
