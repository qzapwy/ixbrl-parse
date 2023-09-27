from typing import List, Type

import pytest

from ixbrlparse import hookimpl
from ixbrlparse.components._base import ixbrlFormat
from ixbrlparse.components.formats import ixtZeroDash
from ixbrlparse.components.transform import get_format
from ixbrlparse.plugins import pm


def test_using_test_plugin():
    class FlurgFormat(ixbrlFormat):
        format_names = ("flurg",)

        def parse_value(self, *_args, **_kwargs) -> str:
            return "flurg"

    class TestPlugin:
        @hookimpl
        def ixbrl_add_formats(self) -> List[Type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    try:
        # check new format is available
        assert get_format("flurg") == FlurgFormat

        # check existing formats are still available
        assert get_format("ixt:zerodash") == ixtZeroDash
    finally:
        pm.unregister(name="flurg")


def test_registering_duplicate_plugin():
    class FlurgFormat(ixbrlFormat):
        format_names = ("ixt:zerodash",)

        def parse_value(self, *_args, **_kwargs) -> str:
            return "flurg"

    class TestPlugin:
        @hookimpl
        def ixbrl_add_formats(self) -> List[Type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    try:
        with pytest.raises(ValueError):
            # check new format is available
            assert get_format("flurg") == FlurgFormat
    finally:
        pm.unregister(name="flurg")