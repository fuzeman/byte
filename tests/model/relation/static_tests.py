"""Relation tests for static models."""
from byte.model import Model
from byte.property import Property


def test_simple_static():
    """Test simple static model relations."""
    class Artist(Model):
        class Options:
            slots = True

        id = Property(int, primary_key=True)

        name = Property(str, max_length=120)

    class Album(Model):
        class Options:
            slots = True

        id = Property(int, primary_key=True)
        artist = Property(Artist)

        title = Property(str, max_length=160)

    class Track(Model):
        class Options:
            slots = True

        id = Property(int, primary_key=True)
        artist = Property(Artist)
        album = Property(Album)

        name = Property(str, max_length=200)

    # Artist
    artist = Artist.create(
        id=1,
        name='Daft Punk'
    )

    assert artist.id == 1
    assert artist.name == 'Daft Punk'

    # Album
    album = Album.create(
        id=1,
        artist=artist,

        title='Discovery'
    )

    assert album.id == 1
    assert album.artist_id == 1

    assert album.artist is artist

    assert album.title == 'Discovery'

    # Track
    track = Track.create(
        id=1,
        artist=artist,
        album=album,

        name='One More Time'
    )

    assert track.id == 1
    assert track.artist_id == 1
    assert track.album_id == 1

    assert track.artist is artist
    assert track.album is album

    assert track.name == 'One More Time'
