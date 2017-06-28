from __future__ import absolute_import, division, print_function

from byte.table import Table
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Table(User)


def test_simple():
    """Test select() query can be created with order."""
    assert_that(users.select().order_by(
        User['id']
    ), has_properties({
        'state': has_entries({
            'order_by': [
                (User['id'], {
                    'order': 'ascending'
                })
            ]
        })
    }))


def test_options_descending():
    """Test select() query can be created with descending order."""
    assert_that(users.select().order_by(
        User['id'].desc()
    ), has_properties({
        'state': has_entries({
            'order_by': equal_to([
                (User['id'], {
                    'order': 'descending'
                })
            ])
        })
    }))
