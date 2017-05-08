from tests.base.models.dynamic.user import User

from byte.collection import Collection

from hamcrest import *

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
