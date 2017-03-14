from byte import Collection, Model, Property

from hamcrest import *


class User(Model):
    id = Property(int, primary_key=True)

    username = Property(str)
    password = Property(str)

users = Collection(User)


def test_simple():
    assert_that(users.select().limit(12), has_properties({
        'state': has_entries({
            'limit': 12
        })
    }))


def test_offset():
    assert_that(users.select().offset(12), has_properties({
        'state': has_entries({
            'offset': 12
        })
    }))
