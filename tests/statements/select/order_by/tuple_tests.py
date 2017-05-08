from tests.base.models.dynamic.user import User

from byte.collection import Collection

from hamcrest import *

users = Collection(User)


def test_simple():
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
