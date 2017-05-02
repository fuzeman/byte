"""Dynamic tests for memory collections."""

from tests.base.core.fixtures import fixture_uri

from byte import Collection, Model, Property
import byte.compilers.simple
import byte.executors.file
import byte.formats.json


@fixture_uri('collections/artists.json')
def test_get_basic(artists_uri):
    """Test basic collections with dynamic models."""
    class Artist(Model):
        class Options:
            collection = Collection(artists_uri, plugins=[
                byte.compilers.simple,
                byte.executors.file,
                byte.formats.json
            ])

        id = Property(int, primary_key=True)
        title = Property(str)

    # Fetch artist, and validate properties
    artist = Artist.Objects.get(1)

    assert artist
    assert artist.id == 1
    assert artist.title == 'Gorillaz'


@fixture_uri('collections/artists.json')
@fixture_uri('collections/albums.json')
@fixture_uri('collections/tracks.json')
def test_get_relations(artists_uri, albums_uri, tracks_uri):
    """Test collection relations with dynamic models."""
    class Artist(Model):
        class Options:
            collection = Collection(artists_uri, plugins=[
                byte.compilers.simple,
                byte.executors.file,
                byte.formats.json
            ])

        id = Property(int, primary_key=True)

        title = Property(str)

    class Album(Model):
        class Options:
            collection = Collection(albums_uri, plugins=[
                byte.compilers.simple,
                byte.executors.file,
                byte.formats.json
            ])

        id = Property(int, primary_key=True)
        artist = Property(Artist)

        title = Property(str)

    class Track(Model):
        class Options:
            collection = Collection(tracks_uri, plugins=[
                byte.compilers.simple,
                byte.executors.file,
                byte.formats.json
            ])

        id = Property(int, primary_key=True)
        artist = Property(Artist)
        album = Property(Album)

        title = Property(str)

    # Fetch track, and ensure relations can be resolved
    track = Track.Objects.get(1)

    assert track
    assert track.id == 1
    assert track.title == 'Ascension (feat. Vince Staples)'

    assert track.artist
    assert track.artist.id == 1
    assert track.artist.title == 'Gorillaz'

    assert track.album
    assert track.album.id == 1
    assert track.album.title == 'Humanz'

    assert track.album.artist
    assert track.album.artist.id == 1
    assert track.album.artist.title == 'Gorillaz'
