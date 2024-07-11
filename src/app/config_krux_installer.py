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
krux_installer.py
"""
import os
import sys
import json
import ctypes
import locale
from functools import partial
from kivy.clock import Clock
from src.utils.trigger import Trigger
from src.app.base_krux_installer import BaseKruxInstaller


class ConfigKruxInstaller(BaseKruxInstaller, Trigger):
    """BaseKruxInstller is the base for Appliction"""

    @staticmethod
    def get_system_lang():
        """Get operational system LANG"""
        if sys.platform in ("linux", "darwin"):
            return os.getenv("LANG")

        if sys.platform == "win32":
            windll = ctypes.windll.kernel32
            return locale.windows_locale[windll.GetUserDefaultUILanguage()]

        raise OSError(f"OS '{sys.platform}' not recognized")

    @staticmethod
    def get_app_dir(name: str) -> str | None:
        """ "Get the full path of config folder"""
        if name not in ("config", "local"):
            raise ValueError(f"Invalid name: '{name}'")

        _system = sys.platform

        if _system in ("linux", "darwin"):
            localappdata = os.path.expanduser("~")
            return os.path.join(localappdata, f".{name}", "krux-installer")

        if _system == "win32":
            if "LOCALAPPDATA" in os.environ:
                localappdata = os.environ["LOCALAPPDATA"]
                if localappdata is not None and localappdata != "":
                    return os.path.join(localappdata, "krux-installer", name)

                raise EnvironmentError("LOCALAPPDATA is empty")

            raise EnvironmentError("LOCALAPPDATA environment variable not found")

        raise OSError(f"Not supported: {sys.platform}")

    @staticmethod
    def create_app_dir(name: str) -> str:
        """ "Create the config folder"""
        path = ConfigKruxInstaller.get_app_dir(name=name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def create_app_file(context: str, name: str) -> str:
        """ "Create config.ini file"""
        path = ConfigKruxInstaller.get_app_dir(name=context)
        file = os.path.join(path, name)
        if not os.path.exists(file):
            with open(file, "w", encoding="utf8") as f:
                f.write("# Generated config. Do not edit this manually!\n")

        return file

    # pylint: disable=signature-differs,arguments-differ
    def get_application_config(self) -> str:
        """Custom path for config.ini"""
        dirname = ConfigKruxInstaller.create_app_dir(name="config")
        self.debug(f"Application directory: {dirname}")

        file = ConfigKruxInstaller.create_app_file(context="config", name="config.ini")
        self.debug(f"ConfigKruxInstaller.get_application_config = {file}")

        return super().get_application_config(file)

    def build_config(self, config):
        """Create default configurations for app"""
        _dir = ConfigKruxInstaller.create_app_dir(name="local")

        config.setdefaults("destdir", {"assets": _dir})
        self.debug(f"{config}.destdir={_dir}")

        baudrate = 1500000
        config.setdefaults("flash", {"baudrate": baudrate})
        self.debug(f"{config}.baudrate={baudrate}")

        lang = ConfigKruxInstaller.get_system_lang()
        config.setdefaults("locale", {"lang": lang})
        self.debug(f"{config}.lang={lang}")

    def build_settings(self, settings):
        """Create settings panel"""
        json_data = [
            {
                "type": "path",
                "title": "Assets's destination path",
                "desc": "Destination path of downloaded assets",
                "section": "destdir",
                "key": "assets",
            },
            {
                "type": "numeric",
                "title": "Flash baudrate",
                "desc": "Applied baudrate during the flash process",
                "section": "flash",
                "key": "baudrate",
            },
            {
                "type": "options",
                "title": "Locale",
                "desc": "Application locale",
                "section": "locale",
                "key": "lang",
                "options": [
                    "af_ZA.UTF-8",
                    "en_US.UTF-8",
                    "es_ES.UTF-8",
                    "fr_FR.UTF-8",
                    "it_IT.UTF-8",
                    "pt_BR.UTF-8",
                    "ru_RU.UTF-8",
                ],
            },
        ]

        json_str = json.dumps(json_data)
        self.debug(f"{settings}.data={json_str}")
        settings.add_json_panel("Settings", self.config, data=json_str)

    def on_config_change(self, config, section, key, value):
        if section == "locale" and key == "lang":
            main = self.screen_manager.get_screen("MainScreen")
            vers = self.screen_manager.get_screen("SelectVersionScreen")
            oldv = self.screen_manager.get_screen("SelectOldVersionScreen")
            warn_stable = self.screen_manager.get_screen(
                "WarningAlreadyDownloadedScreen"
            )
            warn_beta = self.screen_manager.get_screen("WarningBetaScreen")
            verify = self.screen_manager.get_screen("VerifyStableZipScreen")
            unzip = self.screen_manager.get_screen("UnzipStableScreen")

            partials = [
                partial(
                    main.update, name="ConfigKruxInstaller", key="locale", value=value
                ),
                partial(
                    main.update,
                    name="ConfigKruxInstaller",
                    key="version",
                    value=main.version,
                ),
                partial(
                    main.update,
                    name="ConfigKruxInstaller",
                    key="device",
                    value=main.device,
                ),
                partial(
                    main.update, name="ConfigKruxInstaller", key="flash", value=None
                ),
                partial(
                    main.update, name="ConfigKruxInstaller", key="wipe", value=None
                ),
                partial(
                    main.update, name="ConfigKruxInstaller", key="settings", value=None
                ),
                partial(
                    main.update, name="ConfigKruxInstaller", key="about", value=None
                ),
                partial(
                    vers.update, name="ConfigKruxInstaller", key="locale", value=value
                ),
                partial(
                    oldv.update, name="ConfigKruxInstaller", key="locale", value=value
                ),
                partial(
                    warn_stable.update,
                    name="ConfigKruxInstaller",
                    key="locale",
                    value=value,
                ),
                partial(
                    warn_beta.update,
                    name="ConfigKruxInstaller",
                    key="locale",
                    value=value,
                ),
                partial(
                    verify.update, name="ConfigKruxInstaller", key="locale", value=value
                ),
                partial(
                    unzip.update, name="ConfigKruxInstaller", key="locale", value=value
                ),
            ]

            if sys.platform == "linux":
                check = self.screen_manager.get_screen("CheckPermissionsScreen")
                partials.append(
                    partial(
                        check.update,
                        name="ConfigKruxInstaller",
                        key="locale",
                        value=value,
                    )
                )

            for fn in partials:
                Clock.schedule_once(fn, 0)

        else:
            self.debug(f"Skip on_config_change for {section}::{key}={value}")
