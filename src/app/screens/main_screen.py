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
import os
import re
import typing
import sys
from functools import partial
from kivy.clock import Clock
from kivy.app import App
from .base_screen import BaseScreen
from src.utils.constants import VALID_DEVICES_VERSIONS
from src.utils.selector import VALID_DEVICES
from src.i18n import T


class MainScreen(BaseScreen):
    """Main screen is the 'Home' page

    .. versionadded:: 0.0.2-alpha-1
    """

    def __init__(self, **kwargs):
        super().__init__(wid="main_screen", name="MainScreen", **kwargs)

        # Prepare some variables
        self.device = "select a new one"
        self.version = "select a new one"
        self.will_flash = False
        self.will_wipe = False

        # Build grid where buttons will be placed
        self.make_grid(wid="main_screen_grid", rows=6)

        # Buttons will be defined in dynamic way
        # so you will need to keep in mind that
        # some binded methods need a special
        # treatment in loops
        buttons = [
            (
                "main_select_version",
                "".join(
                    [
                        f"[font={self.font}]",
                        f"{self.translate("Version")}: ",
                        "[color=#00AABB]",
                        self.translate(self.version),
                        "[/color]",
                        "[/font]",
                    ]
                ),
                True,
            ),
            (
                "main_select_device",
                "".join(
                    [
                        f"[font={self.font}]",
                        f"{self.translate("Device")}: ",
                        "[color=#00AABB]",
                        self.translate(self.device),
                        "[/color]",
                        "[/font]",
                    ]
                ),
                True,
            ),
            (
                "main_flash",
                "".join(
                    [
                        f"[font={self.font}]",
                        f"[color=#333333]{self.translate("Flash")}[/color]" "[/font]",
                    ]
                ),
                True,
            ),
            (
                "main_wipe",
                "".join(
                    [
                        f"[font={self.font}]",
                        f"[color=#333333]{self.translate("Wipe")}[/color]",
                        "[/font]",
                    ]
                ),
                True,
            ),
            (
                "main_settings",
                "".join([f"[font={self.font}]", self.translate("Settings"), "[/font]"]),
                True,
            ),
            (
                "main_about",
                "".join([f"[font={self.font}]", self.translate("About"), "[/font]"]),
                True,
            ),
        ]

        # START of buttons
        for row, _tuple in enumerate(buttons):

            # START of on_press buttons
            def _press(instance):
                self.debug(f"Calling Button::{instance.id}::on_press")
                if instance.id == "main_flash":
                    if self.will_flash:
                        self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))
                    else:
                        self.warning(f"Button::{instance.id} disabled")

                if instance.id == "main_wipe":
                    if self.will_wipe:
                        self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))
                    else:
                        self.warning(f"Button::{instance.id} disabled")

                if instance.id == "main_select_version":

                    self.ids[instance.id].text = "\n".join(
                        [
                            f"[font={self.font}]",
                            f"[size={self.SIZE_M}sp]",
                            "[color=#efcc00]",
                            f"[b]{self.translate("Fetching data from")}[/b]",
                            "[/color]",
                            "[/size]",
                            f"[size={self.SIZE_MP}sp]",
                            "[color=#efcc00]",
                            "https://api.github.com/repos/selfcustody/krux/releases",
                            "[/color]",
                            "[/size]",
                            "[/font]",
                        ]
                    )

                if instance.id in (
                    "main_select_device",
                    "main_select_version",
                    "main_settings",
                    "main_about",
                ):
                    self.set_background(wid=instance.id, rgba=(0.25, 0.25, 0.25, 1))

            # END of on_press buttons

            # START of on_release_buttons
            def _release(instance):
                self.debug(f"Calling Button::{instance.id}::on_release")
                if instance.id == "main_select_device":
                    select_device = self.manager.get_screen("SelectDeviceScreen")
                    fn = partial(
                        select_device.update,
                        name=self.name,
                        key="version",
                        value=self.version,
                    )
                    Clock.schedule_once(fn, 0)
                    self.set_background(wid="main_select_device", rgba=(0, 0, 0, 1))
                    self.set_screen(name="SelectDeviceScreen", direction="left")

                elif instance.id == "main_select_version":
                    select_version = self.manager.get_screen("SelectVersionScreen")
                    select_version.clear()
                    select_version.fetch_releases()
                    self.set_background(wid="main_select_version", rgba=(0, 0, 0, 1))
                    self.set_screen(name="SelectVersionScreen", direction="left")
                    self.update(name=self.name, key="version", value=self.version)

                elif instance.id == "main_flash":
                    if self.will_flash:
                        # do a click effect
                        self.set_background(wid="main_flash", rgba=(0, 0, 0, 1))

                        # partials are functions that call `update`
                        # method in screen before go to them
                        partials = []

                        # Check if any release file exists
                        if re.findall(r"^v\d+\.\d+\.\d$", self.version):
                            resources = MainScreen.get_destdir_assets()
                            zipfile = os.path.join(
                                resources, f"krux-{self.version}.zip"
                            )
                            if os.path.isfile(zipfile):
                                to_screen = "WarningAlreadyDownloadedScreen"
                            else:
                                to_screen = "DownloadStableZipScreen"

                            screen = self.manager.get_screen(to_screen)
                            partials.append(
                                partial(
                                    screen.update,
                                    name=self.name,
                                    key="version",
                                    value=self.version,
                                )
                            )

                        # check if release is beta
                        elif re.findall("^odudex/krux_binaries", self.version):
                            to_screen = "DownloadBetaScreen"
                            screen = self.manager.get_screen(to_screen)
                            partials.append(
                                partial(
                                    screen.update,
                                    name=self.name,
                                    key="firmware",
                                    value="kboot.kfpkg",
                                )
                            )
                            partials.append(
                                partial(
                                    screen.update,
                                    name=self.name,
                                    key="device",
                                    value=self.device,
                                )
                            )
                            partials.append(
                                partial(screen.update, name=self.name, key="downloader")
                            )

                        # Execute the partials
                        for fn in partials:
                            Clock.schedule_once(fn, 0)

                        # Goto the selected screen
                        self.set_screen(name=to_screen, direction="left")
                    else:
                        self.debug(f"Button::{instance.id} disabled")

                elif instance.id == "main_wipe":
                    if self.will_wipe:
                        # do a click effect
                        self.set_background(wid="main_wipe", rgba=(0, 0, 0, 1))

                        # partials are functions that call `update`
                        # method in screen before go to them
                        partials = []

                        to_screen = "WipeScreen"
                        screen = self.manager.get_screen(to_screen)
                        baudrate = MainScreen.get_baudrate()
                        partials.append(
                            partial(
                                screen.update,
                                name=self.name,
                                key="device",
                                value=self.device,
                            )
                        )
                        partials.append(
                            partial(
                                screen.update,
                                name=self.name,
                                key="wiper",
                                value=baudrate,
                            )
                        )
                        # Execute the partials
                        for fn in partials:
                            Clock.schedule_once(fn, 0)

                        self.set_background(wid="main_wipe", rgba=(0, 0, 0, 1))
                        self.set_screen(name=to_screen, direction="left")
                    else:
                        self.debug(f"Button::{instance.id} disabled")

                elif instance.id == "main_settings":
                    self.set_background(wid="main_settings", rgba=(0, 0, 0, 1))
                    MainScreen.open_settings()

                elif instance.id == "main_about":
                    self.set_background(wid="main_about", rgba=(0, 0, 0, 1))
                    self.set_screen(name="AboutScreen", direction="left")

            # END of on_release buttons

            self.make_button(
                row=row,
                id=_tuple[0],
                root_widget="main_screen_grid",
                text=_tuple[1],
                markup=_tuple[2],
                on_press=_press,
                on_release=_release,
            )
        # END of buttons

    @property
    def device(self) -> str:
        """Getter for device property"""
        return self._device

    @device.setter
    def device(self, value: str):
        self.debug(f"device = {value}")
        self._device = value

    @property
    def version(self) -> str:
        """Getter for version property"""
        return self._version

    @version.setter
    def version(self, value: str):
        """Setter for version property"""
        self.debug(f"version = {value}")
        self._version = value

    @property
    def will_flash(self) -> bool:
        """Getter for will_flash property"""
        return self._will_flash

    @will_flash.setter
    def will_flash(self, value: bool):
        """Setter for will_flash property"""
        self.debug(f"will_flash = {value}")
        self._will_flash = value

    @property
    def will_wipe(self) -> bool:
        """Getter for will_wipe property"""
        return self._will_wipe

    @will_wipe.setter
    def will_wipe(self, value: bool):
        """Setter for will_wipe property"""
        self.debug(f"will_wipe = {value}")
        self._will_wipe = value

    def update(self, *args, **kwargs):
        """Update buttons from selected device/versions on related screens"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        # Check if update to screen
        if name in (
            "KruxInstallerApp",
            "ConfigKruxInstaller",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(msg=f"Invalid screen name: {name}")

        # Check locale
        if key == "locale":
            self.locale = value

        # Check if update to given key
        elif key == "version":

            if value is not None:
                self.version = value
                self.ids["main_select_version"].text = "".join(
                    [
                        f"[font={self.font}]",
                        f"{self.translate("Version")}: ",
                        "[color=#00AABB]",
                        value,
                        "[/color]",
                        "[/font]",
                    ]
                )
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "device":

            # check if update to given values
            if value in VALID_DEVICES:
                self.device = value
                self.will_flash = True
                self.will_wipe = True
                self.ids["main_flash"].text = "".join(
                    [f"[font={self.font}]", self.translate("Flash"), "[/font]"]
                )
                self.ids["main_wipe"].text = "".join(
                    [f"[font={self.font}]", self.translate("Wipe"), "[/font]"]
                )

            else:
                self.will_flash = False
                self.will_wipe = False
                self.ids["main_flash"].markup = True
                self.ids["main_wipe"].markup = True
                self.ids["main_flash"].text = "".join(
                    [
                        f"[font={self.font}]",
                        "[color=#333333]",
                        self.translate("Flash"),
                        "[/color]",
                        "[/font]",
                    ]
                )
                self.ids["main_wipe"].text = "".join(
                    [
                        f"[font={self.font}]",
                        "[color=#333333]",
                        self.translate("Wipe"),
                        "[/color]",
                        "[/font]",
                    ]
                )

            if value == "select a new one":
                value = self.translate("select a new one")

            if value is not None:
                self.ids["main_select_device"].text = "".join(
                    [
                        f"[font={self.font}]",
                        f"{self.translate("Device")}: ",
                        "[color=#00AABB]",
                        value,
                        "[/color]" "[/font]",
                    ]
                )

        elif key == "flash":
            if not self.will_flash:
                self.ids["main_flash"].text = "".join(
                    [
                        f"[font={self.font}]",
                        "[color=#333333]",
                        self.translate("Flash"),
                        "[/color]",
                        "[/font]",
                    ]
                )
            else:
                self.ids["main_flash"].text = "".join(
                    [f"[font={self.font}]", self.translate("Flash"), "[/font]"]
                )

        elif key == "wipe":
            if not self.will_wipe:
                self.ids["main_wipe"].text = "".join(
                    [
                        f"[font={self.font}]",
                        "[color=#333333]",
                        self.translate("Wipe"),
                        "[/color]",
                        "[/font]",
                    ]
                )
            else:
                self.ids["main_wipe"].text = "".join(
                    [f"[font={self.font}]", self.translate("Wipe"), "[/font]"]
                )

        elif key == "settings":
            self.ids["main_settings"].text = "".join(
                [f"[font={self.font}]", self.translate("Settings"), "[/font]"]
            )

        elif key == "about":
            self.ids["main_about"].text = "".join(
                [f"[font={self.font}]", self.translate("About"), "[/font]"]
            )

        else:
            self.redirect_error(msg=f'Invalid key: "{key}"')
