#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiodiscover


def test_get_module_version():
    """Verify get_module_version does not throw."""
    assert aiodiscover.get_module_version() == aiodiscover.__version__
