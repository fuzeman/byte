from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from byte.core.models.expressions.proxy import ProxyEqual, ProxyLessThan, ProxyNotEqual, ProxyOr
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_or():
    """Test select() query can be created with an OR operator inside a string expression."""
    query = users.select().where(
        'id < 35 or username == "alpha"'
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                ProxyOr(
                    ProxyLessThan(User.Properties.id, 35),
                    ProxyEqual(User.Properties.username, 'alpha')
                )
            ]
        })
    }))


def test_or_brackets():
    """Test select() query can be created with an OR operator and brackets inside a string expression."""
    query = users.select().where(
        'id < 35 AND (username != "alpha" or password == "beta") AND password ne "alpha"'
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                ProxyLessThan(User.Properties.id, 35),
                ProxyOr(
                    ProxyNotEqual(User.Properties.username, 'alpha'),
                    ProxyEqual(User.Properties.password, 'beta')
                ),
                ProxyNotEqual(User.Properties.password, 'alpha')
            ]
        })
    }))


def test_parameters():
    """Test select() query can be created with parameters inside a string expression."""
    query = users.select().where(
        'id < ? AND username != ?',
        (35, 'alpha')
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                ProxyLessThan(User.Properties.id, 35),
                ProxyNotEqual(User.Properties.username, 'alpha')
            ]
        })
    }))
