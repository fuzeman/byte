from __future__ import absolute_import, division, print_function

from byte.database import Database
from byte.table import Table
from tests.base.core.fixtures import get_fixture_uri
from tests.base.models.dynamic.album import Album
from tests.base.models.dynamic.artist import Artist
from tests.base.models.dynamic.track import Track
import byte.compilers.operation
import byte.executors.file


def test_get():
    """Test collection with dynamic models."""
    with get_fixture_uri('databases/music', scheme='file.json') as database_uri:
        database = Database(database_uri, [
            Table(Artist, name='artists'),
            Table(Album, name='albums'),
            Table(Track, name='tracks')
        ], plugins=[
            byte.compilers.operation,
            byte.executors.file
        ])

        # Configure relations
        database['albums'].connect(
            artist=database['artists']
        )

        database['tracks'].connect(
            artist=database['artists'],
            album=database['albums']
        )

        # Fetch album, and validate properties
        album = database['albums'].get(Album['id'] == 1)

        assert album
        assert album.id == 1
        assert album.title == 'Humanz'

        assert album.artist
        assert album.artist.id == 1
        assert album.artist.title == 'Gorillaz'
