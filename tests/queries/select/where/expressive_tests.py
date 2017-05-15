from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from byte.core.models.expressions.proxy import ProxyEqual, ProxyGreaterThanOrEqual, ProxyLessThan, ProxyNotEqual
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_simple():
    """Test select() query can be created with expressions."""
    assert_that(users.select().where(
        User['id'] < 35,
        User['username'] != 'alpha'
    ), has_properties({
        'state': has_entries({
            'where': [
                ProxyLessThan(User.Properties.id, 35),
                ProxyNotEqual(User.Properties.username, 'alpha')
            ]
        })
    }))


def test_chain():
    """Test select() query can be created with chained expressions."""
    assert_that(users.select().where(
        User['id'] >= 12
    ).where(
        User['username'] != 'beta'
    ), has_properties({
        'state': has_entries({
            'where': [
                ProxyGreaterThanOrEqual(User.Properties.id, 12),
                ProxyNotEqual(User.Properties.username, 'beta')
            ]
        })
    }))


def test_match():
    """Test select() query can be created with property matching expressions."""
    assert_that(users.select().where(
        User['username'] == User['password']
    ), has_properties({
        'state': has_entries({
            'where': [
                ProxyEqual(User.Properties.username, User.Properties.password)
            ]
        })
    }))
