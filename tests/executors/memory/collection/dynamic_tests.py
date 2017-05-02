"""Dynamic tests for memory collections."""

from byte import Collection, Model, Property
import byte.compilers.simple
import byte.executors.memory


def test_basic():
    """Test basic collections with dynamic models."""
    class Artist(Model):
        class Options:
            collection = Collection('memory://', plugins=[
                byte.compilers.simple,
                byte.executors.memory
            ])

        id = Property(int, primary_key=True)
        name = Property(str)

    # Update memory collection
    Artist.Objects.executor.update({
        1: {
            'id': 1,
            'name': 'Daft Punk'
        }
    })

    # Fetch artist, and validate properties
    artist = Artist.Objects.get(1)

    assert artist
    assert artist.id == 1
    assert artist.name == 'Daft Punk'


def test_relations():
    """Test collection relations with dynamic models."""
    class Artist(Model):
        class Options:
            collection = Collection('memory://', plugins=[
                byte.compilers.simple,
                byte.executors.memory
            ])

        id = Property(int, primary_key=True)

        name = Property(str)

    class Album(Model):
        class Options:
            collection = Collection('memory://', plugins=[
                byte.compilers.simple,
                byte.executors.memory
            ])

        id = Property(int, primary_key=True)
        artist = Property(Artist)

        title = Property(str)

    class Track(Model):
        class Options:
            collection = Collection('memory://', plugins=[
                byte.compilers.simple,
                byte.executors.memory
            ])

        id = Property(int, primary_key=True)
        artist = Property(Artist)
        album = Property(Album)

        name = Property(str)

    # Create objects
    Artist.create(
        id=1,
        name='Daft Punk'
    )

    Album.create(
        id=1,
        artist_id=1,

        title='Discovery'
    )

    Track.create(
        id=1,
        artist_id=1,
        album_id=1,

        name='One More Time'
    )

    # Fetch track, and ensure relations can be resolved
    track = Track.Objects.get(1)

    assert track.id == 1

    assert track.artist.id == 1

    assert track.album.id == 1
    assert track.album.artist.id == 1
