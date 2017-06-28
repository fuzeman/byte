from __future__ import absolute_import, division, print_function

from byte.database import Database
from byte.table import Table
from tests.base.models.dynamic.artist import Artist
import byte.compilers.operation
import byte.executors.memory


def test_basic():
    """Test collection with dynamic models."""
    database = Database('memory://', [
        Table(Artist, name='artists')
    ], plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    # Insert item
    database['artists'].executor.items.update({
        1: {
            'id': 1,
            'title': 'Daft Punk'
        }
    })

    # Fetch artist, and validate properties
    artist = database['artists'].get(Artist['id'] == 1)

    assert artist
    assert artist.id == 1
    assert artist.title == 'Daft Punk'
