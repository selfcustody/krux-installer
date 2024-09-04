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
about_screen.py
"""
from src.app.screens.base_screen import BaseScreen


class WarningBetaScreen(BaseScreen):
    """WarningBetaScreen warns user about krux beta versions"""

    def __init__(self, **kwargs):
        super().__init__(wid="warning_beta_screen", name="WarningBetaScreen", **kwargs)
        self.make_grid(wid="warning_beta_screen_grid", rows=2)

        warning = self.translate("WARNING")
        test_repo = self.translate("This is our test repository")
        unsg_bin = self.translate(
            "These are unsigned binaries for the latest and most experimental features"
        )
        just_try = self.translate(
            "and it's just for trying new things and providing feedback."
        )

        proceed = self.translate("Proceed")
        back = self.translate("Back")

        text = "".join(
            [
                f"[size={self.SIZE_MM}sp]",
                "[color=#efcc00]",
                f"[b]{warning}[/b]",
                "[/color]",
                "[/size]",
                "\n",
                "\n",
                f"[size={self.SIZE_M}sp]",
                f"[color=#efcc00]{test_repo}[/color]",
                "[/size]",
                "\n",
                f"[size={self.SIZE_MP}sp]{unsg_bin}[/size]",
                "\n",
                f"[size={self.SIZE_MP}sp]{just_try}[/size]",
                "\n",
                "\n",
                f"[size={self.SIZE_MM}sp]",
                "[color=#00ff00]",
                f"[u]{proceed}[/u]",
                "[/color]",
                "        ",
                "[color=#ff0000]",
                f"[u]{back}[/u]",
                "[/color]",
                "[/size]",
            ]
        )

        # START of on_press buttons
        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

        # END of on_press buttons

        # START of on_release_buttons
        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
            self.set_screen(name="MainScreen", direction="right")

        self.make_button(
            row=0,
            wid="warning_beta_screen_warn",
            root_widget="warning_beta_screen_grid",
            text=text,
            on_press=_press,
            on_release=_release,
        )

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in ("ConfigKruxInstaller",):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            if value is not None:
                self.locale = value
                self.show_warning()

            else:
                self.redirect_error(f"Invalid value for key {key}: {value}")

        else:
            self.redirect_error(f'Invalid key: "{key}"')

    def show_warning(self):
        """
        Create a warning message where it's content is about
        the beta (and unsigned) firmware
        """
        warning = self.translate("WARNING")
        test_repo = self.translate("This is our test repository")
        unsg_bin = self.translate(
            "These are unsigned binaries for the latest and most experimental features"
        )
        just_try = self.translate(
            "and it's just for trying new things and providing feedback."
        )
        proceed = self.translate("Proceed")
        back = self.translate("Back")

        text = "".join(
            [
                f"[size={self.SIZE_MM}sp][color=#efcc00][b]{warning}[/b][/color][/size]",
                "\n",
                "\n",
                f"[size={self.SIZE_M}sp][color=#efcc00]{test_repo}[/color][/size]",
                "\n",
                f"[size={self.SIZE_MP}sp]{unsg_bin}[/size]",
                "\n",
                f"[size={self.SIZE_MP}sp]{just_try}[/size]",
                "\n",
                "\n",
                f"[size={self.SIZE_MM}sp]",
                f"[color=#00ff00]{proceed}[/color]        [color=#ff0000]{back}[/color]",
                "[/size]",
            ]
        )

        self.ids["warning_beta_screen_warn"].text = text
