"""Basic tests for collections."""

from byte import Collection, Model, Property
import byte.executors.memory


def test_simple():
    """Test basic collections with dynamic models."""
    class Artist(Model):
        class Options:
            collection = Collection('memory://', plugins=[
                byte.executors.memory
            ])

        id = Property(int, primary_key=True)
        name = Property(str)

    # Update memory collection
    Artist.Objects.executor.items = {
        1: {
            'id': 1,
            'name': 'Daft Punk'
        }
    }

    # Fetch artist, and validate properties
    artist = Artist.Objects.get(1)

    assert artist
    assert artist.id == 1
    assert artist.name == 'Daft Punk'
