from byte import Collection, Model, Property
from byte.expressions import And, Equal, GreaterThan, GreaterThanOrEqual, LessThan, NotEqual, Or

from hamcrest import *


class User(Model):
    id = Property(int, primary_key=True)

    username = Property(str)
    password = Property(str)

users = Collection(User)


def test_or():
    query = users.select().where(
        'id < 35 or username == "alpha"'
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                Or(
                    LessThan(User.Properties.id, 35),
                    Equal(User.Properties.username, 'alpha')
                )
            ]
        })
    }))


def test_or_brackets():
    query = users.select().where(
        'id < 35 AND (username != "alpha" or password == "beta") AND password ne "alpha"'
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                LessThan(User.Properties.id, 35),
                Or(
                    NotEqual(User.Properties.username, 'alpha'),
                    Equal(User.Properties.password, 'beta')
                ),
                NotEqual(User.Properties.password, 'alpha')
            ]
        })
    }))


def test_parameters():
    query = users.select().where(
        'id < ? AND username != ?',
        (35, 'alpha')
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                LessThan(User.Properties.id, 35),
                NotEqual(User.Properties.username, 'alpha')
            ]
        })
    }))
