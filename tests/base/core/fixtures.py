from tests.base.core.helpers import FIXTURES_PATH, copy_tree, uri_from_path

from contextlib import contextmanager
from tempfile import NamedTemporaryFile, mkdtemp
import functools
import logging
import os
import shutil

log = logging.getLogger(__name__)


def fixture_content(path, copy=True):
    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            # Call wrapped function (with resolved fixture uri)
            with get_fixture(path, copy=copy) as test_path:
                return f(
                    open(test_path, 'r').read(),
                    *args, **kwargs
                )

        return inner

    return wrapper


def fixture_path(path, copy=True):
    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            # Call wrapped function (with resolved fixture uri)
            with get_fixture(path, copy=copy) as test_path:
                return f(
                    test_path,
                    *args, **kwargs
                )

        return inner

    return wrapper


def fixture_stream(path, copy=True):
    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            # Call wrapped function (with resolved fixture uri)
            with get_fixture(path, copy=copy) as test_path:
                return f(
                    open(test_path, 'r'),
                    *args, **kwargs
                )

        return inner

    return wrapper


def fixture_uri(path, copy=True):
    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            # Call wrapped function (with resolved fixture uri)
            with get_fixture(path, copy=copy) as test_path:
                return f(
                    *(args + (uri_from_path(test_path),)),
                    **kwargs
                )

        return inner

    return wrapper


@contextmanager
def get_fixture(path, copy=True):
    source_path = os.path.abspath(os.path.join(FIXTURES_PATH, path))

    # Ensure fixture exists
    if not os.path.exists(source_path):
        raise ValueError('Fixture %r doesn\'t exist' % (path,))

    # Return actual fixture path (if `copy` has been disabled)
    if not copy:
        yield source_path
        return

    # Copy fixture to temporary path
    if os.path.isdir(source_path):
        temp_path = copy_fixture_directory(source_path)
    else:
        temp_path = copy_fixture_file(source_path)

    try:
        # Return temporary fixture path
        yield temp_path
    finally:
        # Try delete temporary fixture
        try:
            if os.path.isdir(temp_path):
                shutil.rmtree(temp_path)
            else:
                os.remove(temp_path)
        except Exception as ex:
            log.warn('Unable to delete temporary fixture: %s', ex, exc_info=True)


def copy_fixture_directory(source_path):
    temp_path = mkdtemp()

    # Copy contents of `path` into temporary directory
    copy_tree(source_path, temp_path)

    # Return temporary fixture path
    return temp_path


def copy_fixture_file(source_path):
    _, ext = os.path.splitext(source_path)

    # Create copy of fixture to temporary path
    with NamedTemporaryFile(suffix=ext, delete=False) as tp:
        with open(source_path, 'r') as fp:
            tp.write(fp.read())

        temp_path = tp.name

    # Return temporary fixture path
    return temp_path
