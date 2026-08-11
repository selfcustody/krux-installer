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
        When application start, after greeting user with the krux logo, it will
        show the disclaimer. Only when the user accepts it the app will need to
        check if user is running app in linux or non-linux. If running in linux,
        the user will be redirect to CheckPermissionsScreen and then to
        MainScreen. Win32 and Mac will be redirect to MainScreen.
        """
        fn_0 = partial(self.update, name=self.name, key="canvas")
        fn_1 = partial(self.update, name=self.name, key="disclaimer")
        Clock.schedule_once(fn_0, 0)
        Clock.schedule_once(fn_1, 2.1)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """
        After show krux logo, show the disclaimer. Once DisclaimerScreen is
        accepted it asks back for the permission check:
        - in linux, if the current user is in dialout group to allow sudoless flash
        - then go directly to MainScreen
        """
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "disclaimer":
                self.set_screen(name="DisclaimerScreen", direction="left")

            if key == "check-permission":
                self.check_dialout_permission()

        setattr(GreetingsScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("KruxInstallerApp", "DisclaimerScreen", self.name),
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

            # Every family is matched on both "ID" and "ID_LIKE", and the
            # branches form one chain rather than a run of independent ifs.
            # Testing "ID_LIKE" alone left Red Hat Enterprise Linux out: it
            # sets ID="rhel" with ID_LIKE="fedora", so the app ended on the
            # error screen at startup while its derivatives, which carry
            # "rhel" inside ID_LIKE, worked. The Fedora test was also an elif
            # hanging off the SUSE one, and matched only because Fedora ships
            # no ID_LIKE at all.
            distro = os_data.get("ID", "")
            like = os_data.get("ID_LIKE", "")
            name = distro or like

            # Debian and Debian-based systems (PopOS, Ubuntu, Linux Mint, etc.)
            if distro == "debian" or "debian" in like:
                detected = (name, "dialout")

            # Red Hat Enterprise Linux and its rebuilds (CentOS, Rocky, Alma)
            elif distro == "rhel" or "rhel" in like:
                detected = (name, "dialout")

            # Fedora, to fix issue #115
            # see https://github.com/selfcustody/krux-installer/issues/115
            elif "fedora" in distro or "fedora" in like:
                detected = (name, "dialout")

            # SUSE-based systems (openSUSE, SUSE Linux Enterprise)
            elif "suse" in distro or "suse" in like:
                detected = (name, "dialout")

            # Arch, Artix, Manjaro, Slackware, Gentoo. Artix was already
            # handled by AskPermissionDialoutScreen.detect_usermod_bin, but
            # this check runs first and ended the flow before it
            elif distro in ("arch", "artix", "manjaro", "slackware", "gentoo"):
                detected = (name, "uucp")

            # For Alpine, Clear Linux, Solus, etc.
            elif distro in ("alpine", "clear-linux", "solus"):
                detected = (name, "dialout")

            # Check for NixOS 25.11 and allow it
            elif distro == "nixos":
                id_version = os_data.get("VERSION_ID", "unknown version")
                detected = (name, "dialout")
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
            # pylint: disable=import-outside-toplevel
            import grp
            import pwd
        except ImportError:
            return _in_dialout

        # gr_mem lists supplementary members only, so an account whose primary
        # group is the target one was reported as absent even though it already
        # holds serial access. The app then asked for a root usermod on every
        # launch, and that usermod does not add the account to gr_mem when the
        # group is its primary, so the prompt returned on the next launch.
        try:
            if pwd.getpwnam(user).pw_gid == grp.getgrnam(group).gr_gid:
                self.info(f"'{user}' has '{group}' as primary group")
                return True
        except KeyError:
            pass

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
            # pylint: disable=import-outside-toplevel
            import pwd

            # Resolved from the running process, not from $USER. That value is
            # set by whatever launched the application -- a .profile, a
            # .desktop entry, a wrapper on PATH -- and it ends up as the
            # argument of a usermod run as root, so a session-level change
            # could hand permanent access to every serial device on the host
            # to an account the user never named.
            _user = pwd.getpwuid(os.getuid()).pw_name

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
