from byte import Collection, Model, Property
from byte.expressions import Equal, GreaterThan, GreaterThanOrEqual, LessThan, NotEqual

from hamcrest import *


class User(Model):
    id = Property(int, primary_key=True)

    username = Property(str)
    password = Property(str)

users = Collection(User)


def test_simple():
    assert_that(users.select().where(
        User['id'] < 35,
        User['username'] != 'alpha'
    ), has_properties({
        'state': has_entries({
            'where': [
                LessThan(User.Properties.id, 35),
                NotEqual(User.Properties.username, 'alpha')
            ]
        })
    }))


def test_chain():
    assert_that(users.select().where(
        User['id'] >= 12
    ).where(
        User['username'] != 'beta'
    ), has_properties({
        'state': has_entries({
            'where': [
                GreaterThanOrEqual(User.Properties.id, 12),
                NotEqual(User.Properties.username, 'beta')
            ]
        })
    }))


def test_match():
    assert_that(users.select().where(
        User['username'] == User['password']
    ), has_properties({
        'state': has_entries({
            'where': [
                Equal(User.Properties.username, User.Properties.password)
            ]
        })
    }))
