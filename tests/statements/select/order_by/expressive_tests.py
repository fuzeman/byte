from tests.base.models.dynamic.user import User

from byte.collection import Collection

from hamcrest import *

users = Collection(User)


def test_simple():
    query = users.select().order_by(
        User['id']
    )

    assert_that(query, has_property('state', equal_to({
        'order_by': [
            (User['id'], {
                'order': 'ascending'
            })
        ]
    })))


def test_options_descending():
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
