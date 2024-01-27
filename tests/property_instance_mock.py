"""
property_instance_mock.py

authors: Don Kirkby, Intrastellar Explorer
edited by: qlrd

Changes:

- added `obj_type=None` to avoid pylint warning
W0222: Signature differs from overridden '__get__' method (signature-differs)

- added `_get_child_mock` to mimic class like
https://github.com/python/cpython/blob/main/Lib/unittest/mock.py

Get from https://stackoverflow.com/questions/37553552/assert-that-a-propertymock-
was-called-on-a-specific-instance
"""
from unittest.mock import MagicMock, PropertyMock


class PropertyInstanceMock(PropertyMock):
    """Like PropertyMock, but records the instance that was called."""

    def _get_child_mock(self, /, **kwargs):
        return MagicMock(**kwargs)

    def __get__(self, obj, obj_type=None):
        return self(obj)

    def __set__(self, obj, val):
        self(obj, val)
