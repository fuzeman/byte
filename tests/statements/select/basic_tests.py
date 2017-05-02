from byte.collection import Collection
from byte.model import Model
from byte.property import Property
from byte.statements import SelectStatement

from hamcrest import *


class User(Model):
    id = Property(int, primary_key=True)

    username = Property(str)
    password = Property(str)

users = Collection(User)


def test_all():
    assert_that(users.all(), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ()
        })
    ))


def test_select():
    assert_that(users.select(), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ()
        })
    ))


def test_select_properties():
    assert_that(users.select(
        User['id'],
        User['username']
    ), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ('id', 'username')
        })
    ))


def test_select_names():
    assert_that(users.select(
        'id',
        'username'
    ), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ('id', 'username')
        })
    ))
