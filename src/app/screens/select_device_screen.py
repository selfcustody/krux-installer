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
select_device_screen.py
"""
import re
from functools import partial
from kivy.clock import Clock
from src.utils.constants import VALID_DEVICES_VERSIONS
from src.app.screens.base_screen import BaseScreen


class SelectDeviceScreen(BaseScreen):
    """SelectDeviceScreen is where versions can be selected"""

    def __init__(self, **kwargs):
        super().__init__(
            wid="select_device_screen", name="SelectDeviceScreen", **kwargs
        )
        self.enabled_devices = []
        self.make_grid(wid="select_device_screen_grid", rows=9)

        for row, device in enumerate(
            [
                "m5stickv",
                "amigo",
                "dock",
                "bit",
                "yahboom",
                "cube",
                "wonder_mv",
                "tzt",
                "embed_fire",
            ]
        ):

            def on_press(instance):
                if instance.id in self.enabled_devices:
                    self.debug(f"Calling Button::{instance.id}::on_press")
                    self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

            def on_release(instance):
                if instance.id in self.enabled_devices:
                    self.debug(f"Calling Button::{instance.id}::on_release")
                    self.set_background(wid=instance.id, rgba=(0, 0, 0, 1))
                    device = self.ids[instance.id].text
                    clean_device = SelectDeviceScreen.sanitize_markup(device)
                    self.debug(f"on_release::{instance.id} = {clean_device}")
                    main_screen = self.manager.get_screen("MainScreen")
                    fn = partial(
                        main_screen.update,
                        name=self.name,
                        key="device",
                        value=clean_device,
                    )
                    Clock.schedule_once(fn, 0)
                    self.set_screen(name="MainScreen", direction="right")

            self.make_button(
                row=row,
                wid=f"select_device_{device}",
                root_widget="select_device_screen_grid",
                text="",
                font_factor=28,
                halign=None,
                on_press=on_press,
                on_release=on_release,
                on_ref_press=None,
            )

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update buttons according the valid devices for each compatible version"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "version":
                self.enabled_devices = []

                for device in (
                    "m5stickv",
                    "amigo",
                    "dock",
                    "bit",
                    "yahboom",
                    "cube",
                    "wonder_mv",
                    "tzt",
                    "embed_fire",
                ):
                    cleanre = re.compile("\\[.*?\\]")
                    clean_text = re.sub(cleanre, "", value)
                    if (
                        clean_text in VALID_DEVICES_VERSIONS
                        and device not in VALID_DEVICES_VERSIONS.get(clean_text, [])
                    ):
                        self.ids[f"select_device_{device}"].text = "".join(
                            ["[color=#333333]", device, "[/color]"]
                        )
                    else:
                        self.enabled_devices.append(f"select_device_{device}")
                        self.ids[f"select_device_{device}"].text = device

        setattr(SelectDeviceScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=("ConfigKruxInstaller", "SelectDeviceScreen", "MainScreen"),
            on_update=getattr(SelectDeviceScreen, "on_update"),
        )
