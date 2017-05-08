from tests.base.models.dynamic.artist import Artist

from byte.model import Model
from byte.property import Property


class Album(Model):
    id = Property(int, primary_key=True)
    artist = Property(Artist)

    title = Property(str)
