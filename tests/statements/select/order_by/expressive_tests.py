from byte import Collection, Model, Property

from hamcrest import *


class User(Model):
    id = Property(int, primary_key=True)

    username = Property(str)
    password = Property(str)

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
