# -*- encoding: utf-8 -*-
# InterceptingProxy v0.1.0
# Script of an interceptin proxy
# Copyright © 2017, Regna Cristian.
# See /LICENSE for licensing information.
# This file was adapted from Chris Warrick’s Python Project Template.

"""
Adapt Qt resources to Python version.

:Copyright: © 2017, Regna Cristian.
:License: BSD (see /LICENSE).
"""

__all__ = ()

import sys

if sys.version_info[0] == 2:
    import InterceptingProxy.ui.resources2  # NOQA
elif sys.version_info[0] == 3:
    import InterceptingProxy.ui.resources3  # NOQA
else:
    print('FATAL: python version does not match `2` nor `3`')
    sys.exit(0)
