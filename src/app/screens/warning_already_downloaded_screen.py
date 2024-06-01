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
from functools import partial
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from src.utils.constants import get_name, get_version
from src.app.screens.base_screen import BaseScreen
from src.i18n import T


class WarningAlreadyDownloadedScreen(BaseScreen):
    """WarningAlreadyDownloadedScreen warns user about an asset that is already downloaded"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="warning_already_downloaded_screen",
            name="WarningAlreadyDownloadedScreen",
            **kwargs,
        )

        self.make_grid(wid="warning_already_downloaded_screen_grid", rows=2)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(Window.width, Window.height))

        warning = Label(
            text="",
            markup=True,
            valign="center",
            halign="center",
        )
        warning.id = "warning_label"
        self.ids["warning_already_downloaded_screen_grid"].add_widget(warning)
        self.ids[warning.id] = WeakProxy(warning)

        stack = StackLayout()
        stack.id = "stack_layout_buttons"
        self.ids["warning_already_downloaded_screen_grid"].add_widget(stack)
        self.ids[stack.id] = WeakProxy(stack)

        buttons = [
            ("warning_download_again_button", "Download again", False),
            ("warning_proceed_button", "Proceed with current file", False),
        ]

        for row, _tuple in enumerate(buttons):

            def _press(instance):
                self.debug(f"Calling Button::{instance.id}::on_press")
                self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

            def _release(instance):
                self.debug(f"Calling Button::{instance.id}::on_release")
                self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))

                if instance.id == "warning_download_again_button":
                    main_screen = self.manager.get_screen("MainScreen")
                    download_screen = self.manager.get_screen("DownloadStableZipScreen")
                    fn = partial(
                        download_screen.update, key="version", value=main_screen.version
                    )
                    Clock.schedule_once(fn, 0)
                    self.set_screen(name="DownloadStableZipScreen", direction="right")

                if instance.id == "warning_proceed_button":
                    main_screen = self.manager.get_screen("MainScreen")
                    download_screen = self.manager.get_screen(
                        "DownloadStableZipShaScreen"
                    )
                    fn = partial(
                        download_screen.update, key="version", value=main_screen.version
                    )
                    Clock.schedule_once(fn, 0)
                    self.set_screen(
                        name="DownloadStableZipShaScreen", direction="right"
                    )

            btn = Button(
                text=_tuple[1],
                markup=_tuple[2],
                font_size=Window.size[0] // 30,
                background_color=(0, 0, 0, 1),
                color=(0 if row == 0 else 1, 1 if row == 0 else 0, 0, 1),
                size_hint=(0.5, None),
            )
            btn.id = _tuple[0]
            self.ids["stack_layout_buttons"].add_widget(btn)
            self.ids[btn.id] = WeakProxy(stack)
            btn.bind(on_press=_press)
            btn.bind(on_release=_release)
            setattr(self, f"on_press_{_tuple[0]}", _press)
            setattr(self, f"on_press_{_tuple[1]}", _release)

    def update(self, *args, **kwargs):
        """Update buttons on related screen"""
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check locale
        if key == "version":
            warning = self.translate("Asset already downloaded")
            proceed = self.translate(
                "Do you want to proceed with the same file or do you want to download it again?"
            )
            self.ids["warning_label"].text = "\n".join(
                [
                    f"[size=32sp][color=#efcc00][b]{warning}[/b][/color][/size]",
                    "",
                    f"[size=20sp][color=#efcc00]krux-{value}[/color][/size]",
                    "",
                    f"[size=16sp]{proceed}[/size]",
                ]
            )
