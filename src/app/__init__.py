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
__init__.py
"""
import os
import sys
from functools import partial
from kivy.clock import Clock
from kivy.core.window import Window
from src.app.config_krux_installer import ConfigKruxInstaller
from src.app.screens.greetings_screen import GreetingsScreen
from src.app.screens.check_permissions_screen import CheckPermissionsScreen
from src.app.screens.check_internet_connection_screen import (
    CheckInternetConnectionScreen,
)
from src.app.screens.main_screen import MainScreen
from src.app.screens.select_device_screen import SelectDeviceScreen
from src.app.screens.select_version_screen import SelectVersionScreen
from src.app.screens.select_old_version_screen import SelectOldVersionScreen
from src.app.screens.warning_beta_screen import WarningBetaScreen
from src.app.screens.about_screen import AboutScreen
from src.app.screens.download_stable_zip_screen import DownloadStableZipScreen
from src.app.screens.download_stable_zip_sha256_screen import (
    DownloadStableZipSha256Screen,
)
from src.app.screens.download_stable_zip_sig_screen import DownloadStableZipSigScreen
from src.app.screens.download_selfcustody_pem_screen import DownloadSelfcustodyPemScreen
from src.app.screens.verify_stable_zip_screen import VerifyStableZipScreen
from src.app.screens.unzip_stable_screen import UnzipStableScreen
from src.app.screens.download_beta_screen import DownloadBetaScreen
from src.app.screens.warning_already_downloaded_screen import (
    WarningAlreadyDownloadedScreen,
)
from src.app.screens.flash_screen import FlashScreen
from src.app.screens.wipe_screen import WipeScreen
from src.app.screens.error_screen import ErrorScreen


class KruxInstallerApp(ConfigKruxInstaller):
    """KruxInstallerApp is the Root widget"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        # Window.fullscreen = 'auto'
        print(Window.size)
        # Window.size = (640, 800)
        self.debug(f"Window.size={Window.size}")
        Window.clearcolor = (0.9, 0.9, 0.9, 1)

    def build(self):
        """Create the Root widget with an ScreenManager as manager for its sub-widgets"""
        self.setup_screens()
        self.setup_screen_manager()
        return self.screen_manager

    def on_start(self):
        """When application starts, verify system and check latest firmware version"""
        self.on_greetings()

    def setup_screen_manager(self):
        """Loop through defined screens (if have at lease one) and add it to screen_manager"""
        if len(self.screens) > 0:
            for screen in self.screens:
                msg = f"adding screen '{screen.name}'"
                self.debug(msg)
                self.screen_manager.add_widget(screen)

        else:
            raise RuntimeError("Cannot setup screen_manager: screen list is empty")

    def setup_screens(self):
        """Configure all screens given an OS"""
        self.screens.append(GreetingsScreen())

        if sys.platform == "linux":
            self.screens.append(CheckPermissionsScreen())

        self.screens = self.screens + [
            CheckInternetConnectionScreen(),
            MainScreen(),
            SelectDeviceScreen(),
            SelectVersionScreen(),
            SelectOldVersionScreen(),
            WarningBetaScreen(),
            AboutScreen(),
            DownloadStableZipScreen(),
            DownloadStableZipSha256Screen(),
            DownloadStableZipSigScreen(),
            DownloadSelfcustodyPemScreen(),
            VerifyStableZipScreen(),
            UnzipStableScreen(),
            DownloadBetaScreen(),
            WarningAlreadyDownloadedScreen(),
            FlashScreen(),
            WipeScreen(),
            ErrorScreen(),
        ]

    def on_greetings(self):
        """
        When application start, after greeting user with the krux logo, it will need to check if
        user is running app in linux or non-linux. If running in linux, the user will be
        redirect to CheckPermissionsScreen and then to MainScreen. Win32 and Mac will be
        redirect to MainScreen.
        """

        greetings_screen = self.screen_manager.get_screen("GreetingsScreen")

        fn = partial(
            greetings_screen.update, name="KruxInstallerApp", key="check_permissions"
        )
        Clock.schedule_once(fn, 0)
