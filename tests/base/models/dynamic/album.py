from __future__ import absolute_import, division, print_function

from byte.table import Model, Property
from tests.base.models.dynamic.artist import Artist


class Album(Model):
    id = Property(int, primary_key=True)
    artist = Property(Artist)

    title = Property(str)
