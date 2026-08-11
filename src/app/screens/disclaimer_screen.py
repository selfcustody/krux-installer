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
disclaimer_screen.py
"""

from functools import partial
from kivy.clock import Clock
from src.app.screens.base_screen import BaseScreen


class DisclaimerScreen(BaseScreen):
    """DisclaimerScreen shows the same disclaimer the firmware shows on boot"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="disclaimer_screen",
            name="DisclaimerScreen",
            **kwargs,
        )

        self.make_grid(wid=f"{self.id}_grid", rows=2, resize_canvas=True)
        self.make_image(
            wid=f"{self.id}_warn",
            source=self.warn_img,
            root_widget=f"{self.id}_grid",
        )
        self.build_button()

        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def build_button(self):
        """Build the button that holds the disclaimer and the two choices"""

        def on_ref_press(*args):
            if args[1] == "Close":
                DisclaimerScreen.quit_app()

            if args[1] == "IUnderstand":
                # The dialout check decides between AskPermissionDialoutScreen
                # and MainScreen, and it lives on GreetingsScreen. It is only
                # reached once the disclaimer is accepted, so nothing the user
                # could still refuse runs before this point
                greetings = self.manager.get_screen("GreetingsScreen")
                fn = partial(greetings.update, name=self.name, key="check-permission")
                Clock.schedule_once(fn, 0)

        setattr(DisclaimerScreen, f"on_ref_press_{self.id}_label", on_ref_press)

        self.make_button(
            row=0,
            wid=f"{self.id}_label",
            text=self.make_label_text(),
            font_factor=40,
            halign="center",
            root_widget=f"{self.id}_grid",
            on_press=None,
            on_release=None,
            on_ref_press=getattr(DisclaimerScreen, f"on_ref_press_{self.id}_label"),
        )

        # The other screens break their messages into short lines, but this one
        # is a paragraph whose length changes with the locale. A Button does not
        # wrap on its own, so without an explicit text_size the longest line
        # runs past both window borders
        label = self.ids[f"{self.id}_label"]
        label.valign = "middle"
        label.text_size = (label.width * 0.9, None)

        # pylint: disable=unused-argument
        def on_size(instance, value):
            instance.text_size = (instance.width * 0.9, None)

        label.bind(size=on_size)
        setattr(DisclaimerScreen, f"on_wrap_{self.id}_label", on_size)

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "locale":
                self.ids[f"{self.id}_label"].text = self.make_label_text()

        setattr(DisclaimerScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "DisclaimerScreen",
            ),
            on_update=getattr(DisclaimerScreen, "on_update"),
        )

    def make_label_text(self):
        """Make the disclaimer message and the two choices offered to the user"""
        research = self.translate(
            "Krux is a research and development project, made by nerds "
            "building tools for their own interests, open to the world"
        )
        flaws = self.translate(
            "Innovative features may have undiscovered flaws that endanger funds"
        )
        risk = self.translate("Use it at your own risk")
        close = self.translate("Close")
        understand = self.translate("I understand")

        return "".join(
            [
                f"{research}.",
                "\n",
                "\n",
                f"{flaws}.",
                "\n",
                "\n",
                f"[color=#EFCC00]{risk}.[/color]",
                "\n",
                "\n",
                f"[color=#ffffff][ref=Close][u]{close}[/u][/ref][/color]",
                "        ",
                f"[color=#ffffff][ref=IUnderstand][u]{understand}[/u][/ref][/color]",
            ]
        )
