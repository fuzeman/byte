from __future__ import absolute_import, division, print_function

from byte.table import Table
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Table(User)


def test_simple():
    """Test select() query can be created with order defined by tuple."""
    assert_that(users.select().order_by(
        ('id', 'DESC')
    ), has_properties({
        'state': has_entries({
            'order_by': equal_to([
                (User['id'], {
                    'order': 'descending'
                })
            ])
        })
    }))
