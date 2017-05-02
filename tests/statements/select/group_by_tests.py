from byte.collection import Collection
from byte.model import Model
from byte.property import Property

from hamcrest import *


class User(Model):
    id = Property(int, primary_key=True)

    username = Property(str)
    password = Property(str)

users = Collection(User)
