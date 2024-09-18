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
import threading
import traceback
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from src.app.screens.base_flash_screen import BaseFlashScreen
from src.utils.flasher import Flasher


class FlashScreen(BaseFlashScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="flash_screen", name="FlashScreen", **kwargs)
        self.flasher = Flasher()
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def build_on_data(self):
        """
        Build a streaming IO static method using
        some instance variables for flash procedure
        when KTool.print_callback is called

        (useful for to be used in tests)
        """

        # pylint: disable=unused-argument
        def on_data(*args, **kwargs):
            text = " ".join(str(x) for x in args)
            self.info(text)
            text = FlashScreen.parse_general_output(text)
            text = text.replace("\rProgramming", "Programming")

            if "INFO" in text:
                self.output.append(text)
                if "Rebooting" in text:
                    # pylint: disable=not-callable
                    self.done()

            elif "Programming BIN" in text:
                self.output[-1] = text

            elif "*" in text:
                self.output.append("*")
                self.output.append("")

            if len(self.output) > 10:
                del self.output[:1]

            self.ids[f"{self.id}_info"].text = "\n".join(self.output)

        setattr(FlashScreen, "on_data", on_data)

    def build_on_process(self):
        """
        Build a streaming IO static method using
        some instance variables for flash procedure

        (useful for to be used in tests)
        """

        def on_process(file_type: str, iteration: int, total: int, suffix: str):
            percent = (iteration / total) * 100
            please = self.translate("PLEASE DO NOT UNPLUG YOUR DEVICE")
            flashing = self.translate("Flashing")
            at = self.translate("at")

            self.ids[f"{self.id}_progress"].text = "".join(
                [
                    f"[b]{please}[/b]",
                    "\n",
                    f"{percent:.2f} %",
                    "\n",
                    f"{flashing} ",
                    "[color=#efcc00]",
                    "[b]",
                    file_type,
                    "[/b]",
                    "[/color]",
                    f" {at} ",
                    "[color=#efcc00]",
                    "[b]",
                    suffix,
                    "[/b]",
                    "[/color]",
                ]
            )

        setattr(FlashScreen, "on_process", on_process)

    # pylint: disable=unused-argument
    def on_pre_enter(self, *args):
        self.ids[f"{self.id}_grid"].clear_widgets()
        self.build_on_data()
        self.build_on_process()
        self.build_on_done()

        def on_ref_press(*args):
            if args[1] == "Back":
                self.set_screen(name="MainScreen", direction="right")

            elif args[1] == "Quit":
                App.get_running_app().stop()

            else:
                exc = RuntimeError(f"Invalid ref: {args[1]}")
                self.redirect_exception(exception=exc)

        self.make_subgrid(
            wid=f"{self.id}_subgrid", rows=2, root_widget=f"{self.id}_grid"
        )

        self.make_image(
            wid=f"{self.id}_loader",
            source=self.warn_img,
            root_widget=f"{self.id}_subgrid",
        )

        self.make_button(
            row=1,
            wid=f"{self.id}_progress",
            text="",
            font_factor=32,
            root_widget=f"{self.id}_subgrid",
            halign="center",
            on_press=None,
            on_release=None,
            on_ref_press=on_ref_press,
        )

        self.make_button(
            row=2,
            wid=f"{self.id}_info",
            text="",
            font_factor=72,
            root_widget=f"{self.id}_grid",
            halign="justify",
            on_press=None,
            on_release=None,
            on_ref_press=None,
        )

    # pylint: disable=unused-argument
    def on_enter(self, *args):
        """
        Event fired when the screen is displayed and the entering animation is complete.
        """
        self.done = getattr(FlashScreen, "on_done")
        self.flasher.ktool.__class__.print_callback = getattr(FlashScreen, "on_data")
        on_process = partial(
            self.flasher.flash, callback=getattr(self.__class__, "on_process")
        )
        self.thread = threading.Thread(name=self.name, target=on_process)

        # if anything wrong happen, show it
        def hook(err):
            if not self.is_done:
                trace = traceback.format_exception(
                    err.exc_type, err.exc_value, err.exc_traceback
                )
                msg = "".join(trace[-2:])
                self.error(msg)
                self.redirect_exception(exception=RuntimeError(f"Flash failed: {msg}"))

        # hook what happened
        threading.excepthook = hook

        # start thread
        self.thread.start()

    # pylint: disable=unused-argument
    def update(self, *args, **kwargs):
        """Update screen with firmware key. Should be called before `on_enter`"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "baudrate":
                setattr(self, "baudrate", value)

            if key == "firmware":
                setattr(self, "firmware", value)

            elif key == "flasher":
                self.flasher.firmware = getattr(self, "firmware")
                self.flasher.baudrate = getattr(self, "baudrate")

        setattr(FlashScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "UnzipStableScreen",
                "DownloadBetaScreen",
                "FlashScreen",
            ),
            on_update=getattr(FlashScreen, "on_update"),
        )
