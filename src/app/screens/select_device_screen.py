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
main_screen.py
"""
# pylint: disable=no-name-in-module
import re
from functools import partial
from kivy.clock import Clock
from kivy.cache import Cache
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from src.utils.constants import VALID_DEVICES_VERSIONS
from .base_screen import BaseScreen


class SelectDeviceScreen(BaseScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_device_screen", name="SelectDeviceScreen", **kwargs
        )
        self.enabled_devices = []
        self.make_grid(wid="select_device_screen_grid", rows=6)

        for row, device in enumerate(
            ["m5stickv", "amigo", "dock", "bit", "yahboom", "cube"]
        ):

            def _on_press(instance):
                if instance.id in self.enabled_devices:
                    self.debug(f"Calling Button::{instance.id}::on_press")
                    self.set_background(wid=instance.id, rgba=(0.5, 0.5, 0.5, 0.5))

            def _on_release(instance):
                if instance.id in self.enabled_devices:
                    self.debug(f"Calling Button::{instance.id}::on_release")
                    self.set_background(wid=instance.id, rgba=(0, 0, 0, 0))
                    device = self.ids[instance.id].text
                    self.debug(f"on_release::{instance.id} = {device}")
                    main_screen = self.manager.get_screen("MainScreen")
                    fn = partial(
                        main_screen.update, name=self.name, key="device", value=device
                    )
                    Clock.schedule_once(fn, 0)
                    self.set_screen(name="MainScreen", direction="right")

            self.make_button(
                row=row,
                id=f"select_device_{device}",
                root_widget="select_device_screen_grid",
                text=device,
                markup=True,
                on_press=_on_press,
                on_release=_on_release,
            )

    def update(self, *args, **kwargs):
        """Update buttons according the valid devices for each version"""
        if kwargs.get("key") == "version":
            self.debug(
                f"Updating buttons to fit {kwargs.get("key")} = {kwargs.get("version")}"
            )
            version = kwargs.get("value")
            self.enabled_devices = []
            enabled_devices = VALID_DEVICES_VERSIONS[version]

            for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
                if not device in enabled_devices:
                    self.ids[f"select_device_{device}"].markup = True
                    self.ids[f"select_device_{device}"].text = (
                        f"[color=#333333]{device}[/color]"
                    )
                else:
                    self.enabled_devices.append(f"select_device_{device}")
                    self.ids[f"select_device_{device}"].markup = False
                    self.ids[f"select_device_{device}"].text = device
        else:
            self.warning(f"Skiping update for {kwargs.get("key")}")
