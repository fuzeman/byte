"""Tests for static data models (slots enabled)."""

from byte import Model, Property

from datetime import datetime


def test_create():
    """Test static model generation and the creation of static items."""
    class User(Model):
        class Options:
            slots = True

        id = Property(int, primary_key=True)

        username = Property(str)
        password = Property(str)

        created_at = Property(datetime, default=lambda: datetime.now())
        updated_at = Property(datetime, default=lambda: datetime.now())

    user = User(
        id=1,

        username='one',
        password='hunter12'
    )

    assert user.id == 1

    assert user.username == 'one'
    assert user.password == 'hunter12'

    assert user.created_at
    assert user.updated_at
