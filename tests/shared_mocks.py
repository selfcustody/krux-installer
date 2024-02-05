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
