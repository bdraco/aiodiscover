#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiodiscover import get_module_version


async def test_get_module_version():
    """Verify get_module_version does not throw."""
    assert isinstance(get_module_version(), str)
