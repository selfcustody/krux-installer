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
from .base_krux_installer import BaseKruxInstaller

DEFAULT_BAUDRATE = 1500000
DEFAULT_LOCALE = "en-US"


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
            _kruxappdata = os.path.join(localdata, "krux-installer")
        elif _system == "darwin":
            localdata = os.path.expanduser("~")
            _kruxadata = os.path.join(
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

        config.setdefaults("locale", {"lang": "en-US"})
        self.debug(f"{config}.lang={DEFAULT_LOCALE}")

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
                "options": ["en-US", "pt-BR"]
            }
        ]"""
        self.debug(f"{settings}.data={jsondata}")
        settings.add_json_panel("Settings", self.config, data=jsondata)
