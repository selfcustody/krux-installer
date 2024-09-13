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
from functools import partial
from pysudoer import SudoerLinux
from kivy.clock import Clock
from src.app.screens.base_screen import BaseScreen


class AskPermissionDialoutScreen(BaseScreen):
    """
    AskPermissionDialoutScreen ask for user permission
    to register in dialout group in linux
    """

    def __init__(self, **kwargs):
        super().__init__(
            wid="ask_permission_dialout_screen",
            name="AskPermissionDialoutScreen",
            **kwargs,
        )

        self.user = ""
        self.group = ""
        self.distro = ""

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)

        # These variables will setup the inclusion
        # in dialout group, if necessary
        self._bin = "/usr/bin/usermod"
        self._bin_args = ["-a", "-G"]

        # pylint: disable=unused-argument
        def on_permission_created(output: str):
            logout_msg = self.translate("You may need to logout (or even reboot)")
            backin_msg = self.translate("and back in for the new group to take effect")
            not_worry_msg = self.translate(
                "Do not worry, this message won't appear again"
            )

            self.ids[f"{self.id}_label"].text = "".join(
                [
                    f"[size={self.SIZE_M}sp]",
                    logout_msg,
                    "\n",
                    f"{backin_msg}.",
                    "\n",
                    "\n",
                    f"{not_worry_msg}.",
                    "[/size]",
                ]
            )

        setattr(
            AskPermissionDialoutScreen, "on_permission_created", on_permission_created
        )

        def _on_ref_press(*args):
            if args[1] == "Allow":
                # If user isnt in the dialout group,
                # but the configuration was done correctly
                # create the command
                cmd = [self._bin]
                for a in self._bin_args:
                    cmd.append(a)
                cmd.append(self.group)
                cmd.append(self.user)

                try:
                    self.debug(f"cmd={cmd}")
                    sudoer = SudoerLinux(name=f"Add {self.user} to {self.group}")
                    sudoer.exec(cmd=cmd, env={}, callback=on_permission_created)

                # pylint: disable=broad-exception-caught
                except Exception as err:
                    self.error(str(err))
                    self.redirect_exception(exception=err)

            if args[1] == "Deny":
                AskPermissionDialoutScreen.quit_app()

        self.make_label(
            wid=f"{self.id}_label",
            text="",
            root_widget=f"{self.id}_grid",
            halign="justify",
        )

        setattr(
            AskPermissionDialoutScreen, f"on_ref_press_{self.id}_label", _on_ref_press
        )
        self.ids[f"{self.id}_label"].bind(on_ref_press=_on_ref_press)

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """
        In linux, will check for user permission on group
        dialout (debian-li ke) and uucp (archlinux-like) and
        add user to that group to allow sudoless flash
        """
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "user":
                setattr(self, "user", value)

            if key == "group":
                setattr(self, "group", value)

            if key == "distro":
                setattr(self, "distro", value)

            if key == "screen":
                self.show_warning()

        setattr(AskPermissionDialoutScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "GreetingsScreen",
                "AskPermissionDialoutScreen",
                "ErrorScreen",
            ),
            on_update=getattr(AskPermissionDialoutScreen, "on_update"),
        )

    def show_warning(self):
        """Show a warning in relation to operational system"""
        warn_msg = self.translate("WARNING")
        first_msg = self.translate("This is the first run of KruxInstaller in")
        access_msg = self.translate(
            "and it appears that you do not have privileged access to make flash procedures"
        )
        proceed_msg = self.translate(
            "To proceed, click in the Allow button and a prompt will ask for your password"
        )
        exec_msg = self.translate("to execute the following command")

        self.ids[f"{self.id}_label"].text = "".join(
            [
                f"[size={self.SIZE_G}sp][color=#efcc00]{warn_msg}[/color][/size]",
                "\n",
                f'[size={self.SIZE_MP}sp]{first_msg} "{self.distro}"',
                "\n",
                f"{access_msg}.",
                "\n",
                proceed_msg,
                "\n" f"{exec_msg}:",
                "\n",
                "[color=#00ff00]",
                f"{self._bin} {" ".join(self._bin_args or [])} {self.group} {self.user}",
                "[/color]",
                "[/size]",
                "\n",
                "\n",
                f"[size={self.SIZE_M}]",
                "[color=#00FF00][ref=Allow]Allow[/ref][/color]",
                "        ",
                "[color=#FF0000][ref=Deny]Deny[/ref][/color]",
                "[/size]",
            ]
        )
