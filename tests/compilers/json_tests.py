"""JSON compiler tests."""

from byte import Collection, Model, Property

from six.moves import urllib, urllib_parse


def test_file_single(tmpdir):
    """Test JSON compiler with single file collections."""
    path = tmpdir.join('artists.json')
    path.write('{"1": {"id": 1, "name": "Daft Punk"}}')

    class Artist(Model):
        class Options:
            collection = Collection(urllib_parse.urljoin('file:', urllib.request.pathname2url(str(path))[1:]))

        id = Property(int, primary_key=True)

        name = Property(str)

    # Fetch artist, and validate properties
    artist = Artist.Objects.get(1)

    assert artist
    assert artist.id == 1
    assert artist.name == 'Daft Punk'
