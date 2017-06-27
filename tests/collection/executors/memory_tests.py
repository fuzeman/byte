from __future__ import absolute_import, division, print_function

from byte.table import Table
from tests.base.models.dynamic.album import Album
from tests.base.models.dynamic.artist import Artist
from tests.base.models.dynamic.track import Track
import byte.compilers.operation
import byte.executors.memory


def test_basic():
    """Test collection with dynamic models."""
    artists = Table(Artist, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    # Update memory collection
    artists.executor.update({
        1: {
            'id': 1,
            'title': 'Daft Punk'
        }
    })

    # Fetch artist, and validate properties
    artist = artists.get(Artist['id'] == 1)

    assert artist
    assert artist.id == 1
    assert artist.title == 'Daft Punk'


def test_relations():
    """Test collection relations with dynamic models."""
    # Artists
    artists = Table(Artist, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    # Albums
    albums = Table(Album, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    albums.connect(
        artist=artists
    )

    # Tracks
    tracks = Table(Track, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    tracks.connect(
        artist=artists,
        album=albums
    )

    # Create objects
    artists.create(
        id=1,
        title='Daft Punk'
    )

    albums.create(
        id=1,
        artist_id=1,

        title='Discovery'
    )

    tracks.create(
        id=1,
        artist_id=1,
        album_id=1,

        title='One More Time'
    )

    # Fetch track, and ensure relations can be resolved
    track = tracks.get(Track['id'] == 1)

    assert track.id == 1

    assert track.artist.id == 1

    assert track.album.id == 1
    assert track.album.artist.id == 1
