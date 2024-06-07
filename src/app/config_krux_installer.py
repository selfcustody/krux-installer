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
from functools import partial
from kivy.clock import Clock
from src.app.base_krux_installer import BaseKruxInstaller

if os.name == "posix":
    LANG = os.getenv("LANG")
else:
    import platform

    if platform.system() == "Windows":
        import ctypes
        import locale

        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()
        LANG = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        raise OSError(f"OS '{platform.system()}' not recognized")


DEFAULT_BAUDRATE = 1500000


class ConfigKruxInstaller(BaseKruxInstaller):
    """BaseKruxInstller is the base for Appliction"""

    # pylint: disable=signature-differs,arguments-differ
    def get_application_config(self) -> str:
        """Custom path for config.ini"""
        _system = sys.platform
        localappdata = None
        _kruxappdata = None
        if _system == "linux":
            localappdata = os.path.expanduser("~")
            _kruxappdata = os.path.join(localappdata, ".config", "krux-installer")
        elif _system == "win32":
            localappdata = os.getenv("LOCALAPPDATA")
            _kruxappdata = os.path.join(localappdata, "krux-installer")
        elif _system == "darwin":
            localappdata = os.path.expanduser("~")
            _kruxappdata = os.path.join(
                localappdata, "Library", "Application Support", "krux-installer"
            )
        else:
            raise OSError(f"Not supported: {sys.platform}")

        _kruxconfig = os.path.join(_kruxappdata, "config.ini")

        if not os.path.exists(_kruxappdata):
            os.makedirs(_kruxappdata)

        if not os.path.exists(_kruxconfig):
            with open(_kruxconfig, "w", encoding="utf8"):
                pass

        self.debug(f"ConfigKruxInstaller.get_application_config = {_kruxconfig}")
        return super(BaseKruxInstaller, self).get_application_config(_kruxconfig)

    def build_config(self, config):
        """Create default configurations for app"""
        _system = sys.platform
        localdata = None
        _kruxdata = None
        if _system == "linux":
            localdata = os.path.expanduser("~")
            _kruxdata = os.path.join(localdata, ".local", "krux-installer")
        elif _system == "win32":
            localdata = os.getenv("LOCALAPPDATA")
            _kruxdata = os.path.join(localdata, "krux-installer")
        elif _system == "darwin":
            localdata = os.path.expanduser("~")
            _kruxdata = os.path.join(
                localdata, "Library", "Application Support", "krux-installer"
            )
        else:
            raise OSError(f"Not supported: {sys.platform}")

        if not os.path.exists(_kruxdata):
            os.makedirs(_kruxdata)

        config.setdefaults("destdir", {"assets": _kruxdata})
        self.debug(f"{config}.destdir={_kruxdata}")

        config.setdefaults("flash", {"baudrate": DEFAULT_BAUDRATE})
        self.debug(f"{config}.baudrate={DEFAULT_BAUDRATE}")

        config.setdefaults("locale", {"lang": LANG})
        self.debug(f"{config}.lang={LANG}")

    def build_settings(self, settings):
        """Create settings panel"""
        jsondata = """[
            { 
                "type": "path",
                "title": "Assets's destination path",
                "desc": "Destination path of downloaded assets",
                "section": "destdir",
                "key": "assets"
            },            
            { 
                "type": "numeric",
                "title": "Flash baudrate",
                "desc": "Applied baudrate during the flash process",
                "section": "flash",
                "key": "baudrate"
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
                    "ru_RU.UTF-8"
                ]
            }
        ]"""
        self.debug(f"{settings}.data={jsondata}")
        settings.add_json_panel("Settings", self.config, data=jsondata)

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
            ]

            for fn in partials:
                Clock.schedule_once(fn, 0)
