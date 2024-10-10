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
config_krux_installer.py
"""
import os
import sys
import json
import ctypes
import locale
from functools import partial
from kivy import resources as kv_resources
from kivy.clock import Clock
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.utils.trigger import Trigger
from src.app.base_krux_installer import BaseKruxInstaller


class ConfigKruxInstaller(BaseKruxInstaller, Trigger):
    """ConfigKruxInstller is where all configuration occurs"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # When program is frozen exe
        # try to fix the problem with windows
        # that do not render images on bundled .exe
        # https://stackoverflow.com/questions/71656465/
        # how-to-include-image-in-kivy-application-with-onefile-mode-pyinstaller
        # sys._MEIPASS is a temporary folder for PyInstaller.
        if getattr(sys, "frozen", False):
            # this is a Pyinstaller bundle
            _meipass = getattr(sys, "_MEIPASS")
            self.info(f"Adding resources from {_meipass}")
            kv_resources.resource_add_path(_meipass)
            self.assets_path = os.path.join(_meipass, "assets")
            self.i18n_path = os.path.join(_meipass, "src", "i18n")
        else:
            cwd_path = os.path.dirname(__file__)
            rel_assets_path = os.path.join(cwd_path, "..", "..", "assets")
            rel_i18n_path = os.path.join(cwd_path, "..", "i18n")
            self.assets_path = os.path.abspath(rel_assets_path)
            self.i18n_path = os.path.abspath(rel_i18n_path)

        self.info(f"Registering assets path={self.assets_path}")

        noto_sans_path = os.path.join(self.assets_path, "NotoSansCJK_Cy_SC_KR_Krux.ttf")
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

    @staticmethod
    def make_lang_code(lang: str) -> str:
        """Properly say which language will be used based on system"""
        if sys.platform in ("linux", "darwin"):
            return f"{lang}.UTF-8"

        if sys.platform == "win32":
            return lang

        raise OSError(
            f"Couldn 't possible to setup locale: OS '{sys.platform}' not implemented"
        )

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

        # Check if system lang is supported in src/i18n
        # and if not, defaults to en_US
        if sys.platform in ("linux", "darwin"):
            lang_file = os.path.join(self.i18n_path, f"{lang}.json")
            if os.path.isfile(lang_file):
                config.setdefaults("locale", {"lang": lang})
                self.info(f"{config}.lang={lang}")

            else:
                self.warning(f"{lang} not supported. Default {config}.lang=en_US.UTF-8")
                config.setdefaults("locale", {"lang": "en_US.UTF-8"})

        if sys.platform == "win32":
            lang_file = os.path.join(self.i18n_path, f"{lang}.UTF-8.json")
            if os.path.isfile(lang_file):
                config.setdefaults("locale", {"lang": lang})
                self.info(f"{config}.lang={lang}")

            else:
                self.warning(f"{lang} not supported. Default {config}.lang=en_US")
                config.setdefaults("locale", {"lang": "en_US"})

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
                    ConfigKruxInstaller.make_lang_code("af_ZA"),
                    ConfigKruxInstaller.make_lang_code("en_US"),
                    ConfigKruxInstaller.make_lang_code("es_ES"),
                    ConfigKruxInstaller.make_lang_code("fr_FR"),
                    ConfigKruxInstaller.make_lang_code("it_IT"),
                    ConfigKruxInstaller.make_lang_code("ko_KR"),
                    ConfigKruxInstaller.make_lang_code("nl_NL"),
                    ConfigKruxInstaller.make_lang_code("pt_BR"),
                    ConfigKruxInstaller.make_lang_code("ru_RU"),
                    ConfigKruxInstaller.make_lang_code("zh_CN"),
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
            about = self.screen_manager.get_screen("AboutScreen")
            warn_before = self.screen_manager.get_screen(
                "WarningBeforeAirgapUpdateScreen"
            )

            if sys.platform == "win32":
                value = f"{value}.UTF-8"

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
                partial(
                    about.update, name="ConfigKruxInstaller", key="locale", value=value
                ),
                partial(
                    warn_before.update,
                    name="ConfigKruxInstaller",
                    key="locale",
                    value=value,
                ),
            ]

            if sys.platform == "linux":
                ask = self.screen_manager.get_screen("AskPermissionDialoutScreen")
                partials.append(
                    partial(
                        ask.update,
                        name="ConfigKruxInstaller",
                        key="locale",
                        value=value,
                    )
                )

            for fn in partials:
                Clock.schedule_once(fn, 0)

        else:
            self.debug(f"Skip on_config_change for {section}::{key}={value}")
