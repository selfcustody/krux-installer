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
base_download_screen.py
"""
import typing
from functools import partial
from threading import Thread
from kivy.clock import Clock, ClockEvent
from src.app.screens.base_screen import BaseScreen
from src.utils.downloader.asset_downloader import AssetDownloader


class BaseDownloadScreen(BaseScreen):
    """BaseDownloadScreen setup some initial variables for usable Downloader screens"""

    def __init__(self, wid: str, name: str, **kwargs):
        super().__init__(wid=wid, name=name, **kwargs)
        self.make_grid(wid=f"{self.id}_grid", rows=2)

        self._downloader = None
        self._thread = None
        self._trigger = None
        self.version = None
        self._to_screen = ""

        self.make_button(
            row=0,
            wid=f"{self.id}_progress",
            root_widget=f"{self.id}_grid",
            halign=None,
            text="",
            font_factor=18,
            on_press=None,
            on_release=None,
            on_ref_press=None,
        )

        # A little ugly hacky way to join
        # the methods: (1) resize the font;
        # (2) resize canvas. This is needed because
        # when more than one buttons are used, the
        # canvas wasnt properly updated.
        # the bind method is needed only in one
        # of the buttons
        # pylint: disable=unused-argument
        def on_resize(instance, value):
            instance.font_size = BaseScreen.get_half_diagonal_screen_size(18)
            update = getattr(self, "update")
            fn = partial(update, name=self.name, key="canvas")
            Clock.schedule_once(fn, 0)

        self.ids[f"{self.id}_progress"].bind(size=on_resize)

        # information label
        # it has data about url
        # and downloaded paths
        # pylint: disable=unused-argument
        self.make_button(
            row=1,
            wid=f"{self.id}_info",
            root_widget=f"{self.id}_grid",
            font_factor=52,
            halign=None,
            text="",
            on_press=None,
            on_release=None,
            on_ref_press=None,
        )

    @property
    def to_screen(self) -> str:
        """Get where the current screen will go"""
        self.debug(f"getter::to_screen={self._to_screen}")
        return self._to_screen

    @to_screen.setter
    def to_screen(self, value: str):
        """Set where the current screen will go"""
        self.debug(f"setter::to_screen={value}")
        self._to_screen = value

    @property
    def downloader(self) -> AssetDownloader | None:
        """Get an `AssetDownloader`"""
        self.debug(f"getter::downloader={self._downloader}")
        return self._downloader

    @downloader.setter
    def downloader(self, value: AssetDownloader):
        """Set an `AssetDownloader`"""
        self.debug(f"setter::downloader={value}")
        self._downloader = value

    @downloader.deleter
    def downloader(self):
        """Delete an `AssetDownloader`"""
        self.debug(f"deleter::downloader={self._downloader}")
        del self._downloader

    @property
    def thread(self) -> Thread | None:
        """Return a Thread"""
        self.debug(f"getter::thread={self._thread}")
        return self._thread

    @thread.setter
    def thread(self, value: Thread):
        """
        Wait until download thread finish,
        when finished call this callback

        See https://kivy.org/doc/stable/guide/events.html
        """
        self.debug(f"setter::thread={self._thread}->{value}")
        self._thread = value

    @property
    def trigger(self) -> ClockEvent:
        """Trigger is a `ClockEvent` that should be triggered after download is done"""
        self.debug(f"getter::trigger={self._trigger}")
        return self._trigger

    @trigger.setter
    def trigger(self, value: typing.Callable):
        """Create a `ClockEvent` given a callback"""
        self.debug(f"getter::trigger={value}")
        self._trigger = Clock.create_trigger(value)

    @trigger.deleter
    def trigger(self):
        """Delete a `ClockEvent`"""
        self.debug(f"deleter::trigger={self._trigger}")
        del self._trigger

    # pylint: disable=unused-argument
    def on_pre_enter(self, *args):
        """Before enter, reset text to show that its requesting github API"""
        connecting = self.translate("Connecting")
        text = "".join([f"{connecting}..."])
        self.ids[f"{self.id}_progress"].text = text

    # pylint: disable=unused-argument
    def on_enter(self, *args):
        """
        Event fired when the screen is displayed and the entering animation is complete.

        Every inherithed class should implement it own `on_trigger` and `on_progress`
        staticmethods. The method `on_progress` should call `self.trigger` ath the end:
        """
        if self.downloader is not None:
            # on trigger should be defined on inherited classes
            self.trigger = getattr(self.__class__, "on_trigger")

            # on progress should be defined on inherited classes
            download = getattr(self.downloader, "download")
            on_progress = getattr(self.__class__, "on_progress")
            _fn = partial(download, on_data=on_progress)

            # Now run it as a partial function
            # on parallel thread to not block
            # the process during the kivy cycles
            self.thread = Thread(name=self.name, target=_fn)
            self.thread.start()
        else:
            msg = "Downloader isnt configured. Use `update` method first"
            exc = RuntimeError(msg)
            self.error(msg)
            self.redirect_exception(exception=exc)

    def update_download_screen(self, key: str, value: typing.Any):
        """Update a screen in accord with the valid ones"""
        if key == "version":
            build_downloader = getattr(self, "build_downloader")
            build_downloader(value)

        if key == "progress":
            on_download_progress = getattr(self, "on_download_progress")
            on_download_progress(value)

    @staticmethod
    def make_download_info(
        download_msg: str, from_url: str, to_msg: str, to_path: str
    ) -> str:
        """
        download_stable_zip_sha256_screen and download_stable_zip_sig_screen
        use same procedure to update informational content of downloaded file
        """
        return "".join(
            [
                download_msg,
                "\n",
                f"[color=#00AABB][ref={from_url}]{from_url}[/ref][/color]",
                "\n",
                to_msg,
                "\n",
                to_path,
            ]
        )

    @staticmethod
    def make_progress_info(
        of_msg: str,
        percent: float,
        downloaded_len: float,
        content_len: float,
    ) -> str:
        """
        download_stable_zip_sha256_screen and download_stable_zip_sig_screen
        use same procedure to update its progress content of downloaded file
        """
        return "".join(
            [
                f"[b]{percent * 100:,.2f} %[/b]",
                "\n",
                str(downloaded_len),
                f" {of_msg} ",
                str(content_len),
                " B",
            ]
        )
