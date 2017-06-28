from __future__ import absolute_import, division, print_function

import os
import shutil

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

TESTS_PATH = os.path.join(ROOT_PATH, 'tests')
FIXTURES_PATH = os.path.join(TESTS_PATH, '__fixtures__')


def copy_tree(src, dst, symlinks=False, ignore=None):
    """Copy directory tree.

    :param src: Source path
    :type src: str

    :param dst: Destination path
    :type dst: str

    :param symlinks: Copy symbolic links
    :type symlinks: bool

    :param ignore: Ignore function
    :type ignore: function
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
