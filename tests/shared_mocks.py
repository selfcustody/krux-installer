"""
shared_mocks.py

authors[PropertyInstanceMock]:
Don Kirkby, Intrastellar Explorer

authors[MockZipFile]:
nneonneo

edited by: qlrd

Changes[PropertyInstanceMock]:

- added `obj_type=None` to avoid pylint warning
W0222: Signature differs from overridden
'__get__' method (signature-differs)

- added `_get_child_mock` to mimic class like
https://github.com/python/cpython/blob/
main/Lib/unittest/mock.py

Get from https://stackoverflow.com/
questions/37553552/assert-that-a-propertymock-
was-called-on-a-specific-instance
"""

import typing
import sys
from unittest.mock import Mock, MagicMock, PropertyMock


class PropertyInstanceMock(PropertyMock):
    """Like PropertyMock, but records the instance that was called."""

    def _get_child_mock(self, /, **kwargs):
        """return a MagicMock"""
        return MagicMock(**kwargs)

    def __get__(self, obj, obj_type=None):
        """Return a Getter of @property"""
        return self(obj)

    def __set__(self, obj, val):
        """Return a setter of @property.setter"""
        self(obj, val)


class MockZipFile:
    """
    Instead of having mockZip.__enter__ return an empty list,
    have it return an object like the following
    """

    def __init__(self):
        self.files = [
            Mock(filename="README.md"),
            Mock(filename="pyproject.toml"),
            Mock(filename="LICENSE"),
            Mock(filename=".pylintrc"),
        ]

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value: typing.List[Mock]):
        self._files = value

    def __iter__(self):
        return iter(self.files)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def infolist(self):
        return self.files

    def namelist(self):
        return [data.filename for data in self.files]

    def extract(self, name: str, path: str):
        pass


class MockKruxZipFile(MockZipFile):

    def __init__(self):
        super().__init__()
        self.files = [
            Mock(filename="test/"),
            Mock(filename="test/maixpy_m5stickv"),
            Mock(filename="test/maixpy_m5stickv/firmware.bin"),
            Mock(filename="test/maixpy_m5stickv/firmware.bin.sig"),
            Mock(filename="test/maixpy_m5stickv/kboot.kfpkg"),
            Mock(filename="test/maixpy_amigo_tft"),
            Mock(filename="test/maixpy_amigo_tft/firmware.bin"),
            Mock(filename="test/maixpy_amigo_tft/firmware.bin.sig"),
            Mock(filename="test/maixpy_amigo_tft/kboot.kfpkg"),
            Mock(filename="test/maixpy_amigo_ips"),
            Mock(filename="test/maixpy_amigo_ips/firmware.bin"),
            Mock(filename="test/maixpy_amigo_ips/firmware.bin.sig"),
            Mock(filename="test/maixpy_amigo_ips/kboot.kfpkg"),
            Mock(filename="test/maixpy_dock"),
            Mock(filename="test/maixpy_dock/firmware.bin"),
            Mock(filename="test/maixpy_dock/firmware.bin.sig"),
            Mock(filename="test/maixpy_dock/kboot.kfpkg"),
            Mock(filename="test/maixpy_bit"),
            Mock(filename="test/maixpy_bit/firmware.bin"),
            Mock(filename="test/maixpy_bit/firmware.bin.sig"),
            Mock(filename="test/maixpy_bit/kboot.kfpkg"),
            Mock(filename="test/maixpy_yahboom"),
            Mock(filename="test/maixpy_yahboom/firmware.bin"),
            Mock(filename="test/maixpy_yahboom/firmware.bin.sig"),
            Mock(filename="test/maixpy_yahboom/kboot.kfpkg"),
        ]


class MonkeyPort:

    # pylint: disable=too-few-public-methods
    def __init__(self, vid: str, device: str):
        self.vid = vid
        self.device = device


class MockListPortsGrep(MagicMock):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.devices = []

        if sys.platform in ("linux", "darwin"):
            self.devices = [
                MagicMock(vid="0403", device="/mock/path0"),
                MagicMock(vid="0403", device="/mock/path1"),
                MagicMock(vid="7523", device="/mock/path0"),
            ]
        elif sys.platform == "win32":
            self.devices = [
                MagicMock(vid="0403", device="MOCK0"),
                MagicMock(vid="0403", device="MOCK1"),
                MagicMock(vid="7523", device="MOCK0"),
            ]


class MockSerial(MagicMock):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open(self):
        pass

    def close(self):
        pass
