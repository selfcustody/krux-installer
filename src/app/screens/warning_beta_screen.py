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

from src.utils.constants import get_name, get_version
from src.app.screens.base_screen import BaseScreen
from src.i18n import T


class WarningBetaScreen(BaseScreen):
    """WarningBetaScreen warns user about krux beta versions"""

    def __init__(self, **kwargs):
        super().__init__(wid="warning_beta_screen", name="WarningBetaScreen", **kwargs)
        self.make_grid(wid="warning_beta_screen_grid", rows=1)

        warning = self.translate("WARNING")
        test_repo = self.translate("This is our test repository")
        unsg_bin = self.translate(
            "These are unsigned binaries for the latest and most experimental features"
        )
        just_try = self.translate(
            "and it's just for trying new things and providing feedback."
        )

        text = [
            f"[size=32sp][color=#efcc00][b]{warning}[/b][/color][/size]",
            "",
            f"[size=20sp][color=#efcc00]{test_repo}[/color][/size]",
            "",
            f"[size=16sp]{unsg_bin}[/size]",
            f"[size=16sp]{just_try}[/size]",
        ]

        # START of on_press buttons
        def _press(instance):
            self.debug(f"Calling Button::{instance.id}::on_press")
            self.set_background(wid=instance.id, rgba=(0.5, 0.5, 0.5, 0.5))

        # END of on_press buttons

        # START of on_release_buttons
        def _release(instance):
            self.debug(f"Calling Button::{instance.id}::on_release")
            self.set_background(wid=instance.id, rgba=(0, 0, 0, 0))
            self.set_screen(name="MainScreen", direction="right")

        self.make_button(
            row=0,
            id="warning_beta_screen_warn",
            root_widget="warning_beta_screen_grid",
            text="\n".join(text),
            markup=True,
            on_press=_press,
            on_release=_release,
        )

    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in ("ConfigKruxInstaller",):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            self.locale = value
            warning = self.translate("WARNING")
            test_repo = self.translate("This is our test repository")
            unsg_bin = self.translate(
                "These are unsigned binaries for the latest and most experimental features"
            )
            just_try = self.translate(
                "and it's just for trying new things and providing feedback."
            )

            text = [
                f"[size=32sp][color=#efcc00][b]{warning}[/b][/color][/size]",
                "",
                f"[size=20sp][color=#efcc00]{test_repo}[/color][/size]",
                "",
                f"[size=16sp]{unsg_bin}[/size]",
                f"[size=16sp]{just_try}[/size]",
            ]

            self.ids["warning_beta_screen_warn"].text = "\n".join(text)
