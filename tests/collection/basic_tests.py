"""Basic tests for collections."""

from byte import Collection, Model, Property


def test_import_generator():
    """Test collection import generator."""
    class Artist(Model):
        class Options:
            collection = Collection()

        id = Property(int, primary_key=True)

        name = Property(str)

    # Import items into collections
    assert list(Artist.Objects.import_items(
        [{
            'id': 1,
            'name': 'Daft Punk'
        }],
        generator=True
    )) == [
        1
    ]

    # Fetch artist, and validate properties
    artist = Artist.Objects.get(1)

    assert artist.id == 1
    assert artist.name == 'Daft Punk'


def test_import_relations():
    """Test collection import with relations."""
    class Artist(Model):
        class Options:
            collection = Collection()

        id = Property(int, primary_key=True)

        name = Property(str)

    class Album(Model):
        class Options:
            collection = Collection()

        id = Property(int, primary_key=True)
        artist = Property(Artist)

        title = Property(str)

    class Track(Model):
        class Options:
            collection = Collection()

        id = Property(int, primary_key=True)
        artist = Property(Artist)
        album = Property(Album)

        name = Property(str)

    # Import items into collections
    Artist.Objects.import_items([{
        'id': 1,
        'name': 'Daft Punk'
    }])

    Album.Objects.import_items([{
        'id': 1,
        'artist_id': 1,

        'title': 'Discovery'
    }])

    Track.Objects.import_items([{
        'id': 1,
        'artist_id': 1,
        'album_id': 1,

        'name': 'One More Time'
    }])

    # Fetch track, and ensure relations can be resolved
    track = Track.Objects.get(1)

    assert track.id == 1

    assert track.artist.id == 1

    assert track.album.id == 1
    assert track.album.artist.id == 1
