"""byte - compatibility module."""
from __future__ import absolute_import, division, print_function

from byte.core.enums import PythonImplementation

import sys

PY2 = sys.version_info[0] == 2
PY26 = sys.version_info[0:2] == (2, 6)
PY27 = sys.version_info[0:2] == (2, 7)

PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] == (3, 4)

PYPY = hasattr(sys, 'pypy_translation_info')
PYPY2 = PYPY and PY27
PYPY3 = PYPY and PY3


# Python Implementation
def detect_python_implementation():
    if PYPY:
        return PythonImplementation.PyPy

    # Detect with the `platform` module
    try:
        import platform

        if platform.python_implementation() == 'CPython':
            return PythonImplementation.CPython

        if platform.python_implementation() == 'PyPy':
            return PythonImplementation.PyPy
    except Exception:
        return PythonImplementation.Unknown


PYTHON_IMPLEMENTATION = detect_python_implementation()
