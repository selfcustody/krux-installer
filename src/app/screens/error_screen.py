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
error_screen.py
"""
import webbrowser
from src.app.screens.base_screen import BaseScreen


class ErrorScreen(BaseScreen):
    """
    CheckInternetConnectionScreen will check internet connection and get the
    latest release if ok
    """

    def __init__(self, **kwargs):
        super().__init__(
            wid="error_screen",
            name="ErrorScreen",
            **kwargs,
        )
        self.src_code = "https://github.com/selfcustody/krux-installer"

        # Build grid where buttons will be placed
        self.make_grid(wid=f"{self.id}_grid", rows=1)

        # START of on_press buttons
        def on_ref_press(*args):
            if args[1] == "Back":
                self.set_screen(name="GreetingsScreen", direction="right")

            if args[1] == "Quit":
                ErrorScreen.quit_app()

            if args[1] == "ReportIssue":
                webbrowser.open(f"{self.src_code}/issues")

        self.make_button(
            row=0,
            wid=f"{self.id}_label",
            root_widget=f"{self.id}_grid",
            text="",
            font_factor=48,
            halign="center",
            on_press=None,
            on_release=None,
            on_ref_press=on_ref_press,
        )

    @staticmethod
    def chunkstring(string, length):
        """Split a long string into multiline string with equal lengths"""
        return (string[0 + i : length + i] for i in range(0, len(string), length))

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
            if key == "error":
                self.error(str(value))
                stack = str(value).split(":")
                title = stack[0]
                reason = []

                for r in stack[1:]:
                    c = list(ErrorScreen.chunkstring(r, 80))
                    d = "\n".join(c)
                    reason.append(d)

                self.ids[f"{self.id}_label"].text = "".join(
                    [
                        f"[color=#ff0000]{title}[/color]",
                        "\n",
                        "\n".join(reason),
                        "\n",
                        "Report issue at ",
                        "[color=#00aabb]",
                        "[ref=ReportIssue]",
                        f"{self.src_code}/issues",
                        "[/ref]",
                        "[/color]",
                        "\n",
                        "[color=#00FF00]",
                        "[ref=Back]",
                        "[u]Back[/u]",
                        "[/ref]",
                        "[/color]",
                        "        ",
                        "[color=#FF0000]",
                        "[ref=Quit]",
                        "[u]Quit[/u]",
                        "[/ref]",
                    ]
                )

        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=tuple(self.manager.screen_names),
            on_update=on_update,
        )
