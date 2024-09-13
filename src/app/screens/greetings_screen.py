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
    import distro
    import grp


class GreetingsScreen(BaseScreen):
    """GreetingsScreen show Krux logo"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="greetings_screen",
            name="GreetingsScreen",
            **kwargs,
        )

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)

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
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

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
            if key == "canvas":
                fn = partial(self.update, name=self.name, key="check-permission-screen")
                Clock.schedule_once(fn, 2.1)

            if key == "check-permission-screen":
                self.check_permissions_for_dialout_group()

            if key == "check-internet-connection":
                self.check_internet_connection()

        setattr(GreetingsScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("KruxInstallerApp", "GreetingsScreen"),
            on_update=getattr(GreetingsScreen, "on_update"),
        )

    def check_permissions_for_dialout_group(self):
        """
        Here's where the check process start
        first get the current user, then verify
        the linux distribution used and use the
        proper command to add the user in 'dialout'
        group (in some distros, can be 'uucp')
        """
        if sys.platform.startswith("linux"):
            # get current user
            _user = os.environ.get("USER")
            _in_dialout = False
            _group = None

            # detect linux distro
            if distro.id() in ("ubuntu", "fedora", "linuxmint"):
                _group = "dialout"

            elif distro.like() == "debian":
                _group = "dialout"

            elif distro.id() in ("arch", "manjaro", "slackware", "gentoo"):
                _group = "uucp"

            else:
                exc = RuntimeError(f"{distro.name(pretty=True)} not supported")
                self.redirect_exception(exception=exc)

            # loop throug all linux groups and check
            # if the user is registered in the "dialout" group
            for _grp in grp.getgrall():
                if _group == _grp.gr_name:
                    self.debug(f"Found {_grp.gr_name}")
                    for _grpuser in _grp[3]:
                        self.debug(_grpuser)
                        if _grpuser == _user:
                            self.debug(f"'{_user}' already in group '{_group}'")
                            _in_dialout = True

            # if user is not in dialout group, warn user
            # and then redirect to a screen that will
            # proceed with the proper operation
            if not _in_dialout:
                ask = self.manager.get_screen("AskPermissionDialoutScreen")
                _distro = distro.name(pretty=True)

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
                name="KruxInstallerApp",
                key="version",
                value=selector.releases[0],
            )
            Clock.schedule_once(fn, 0)
            self.set_screen(name="MainScreen", direction="left")

        # pylint: disable=broad-exception-caught
        except Exception as exc:
            self.error(str(exc))
            self.redirect_exception(exception=exc)
