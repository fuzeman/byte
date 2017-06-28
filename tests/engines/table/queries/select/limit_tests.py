from __future__ import absolute_import, division, print_function

from byte.table import Table
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Table(User)


def test_simple():
    """Test select() query can be created with limit."""
    assert_that(users.select().limit(12), has_properties({
        'state': has_entries({
            'limit': 12
        })
    }))


def test_offset():
    """Test select() query can be created with offset."""
    assert_that(users.select().offset(12), has_properties({
        'state': has_entries({
            'offset': 12
        })
    }))
