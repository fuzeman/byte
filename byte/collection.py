# -*- coding: utf-8 -*-

"""Contains the collection structure for the storage of keyed items."""

from byte.model import Model

from six import string_types
from six.moves.urllib.parse import urlparse
import inspect
import logging

log = logging.getLogger(__name__)


class CollectionError(Exception):
    """Generic collection error."""


class CollectionLoadError(CollectionError):
    """Collection couldn't be loaded."""


class CollectionModelError(CollectionError):
    """"Collection model violation."""


class CollectionParseError(CollectionError):
    """Collection parse error."""


class CollectionValidationError(CollectionError):
    """Collection item violation error."""


class Collection(object):
    """Collection for the storage of keyed items."""

    def __init__(self, model_or_uri=None, uri=None, model=None, load=True):
        """
        Create keyed item collection.

        :param uri: Data Source URI
        :type uri: str

        :param model: Collection data model
        :type model: class
        """
        self.model = None
        self.uri = None

        # Parse dynamic parameter
        if model_or_uri:
            if inspect.isclass(model_or_uri) and issubclass(model_or_uri, Model):
                self.model = model_or_uri
            elif isinstance(model_or_uri, string_types):
                self.uri = urlparse(model_or_uri)
            else:
                raise ValueError('Unknown initialization parameter value (expected subclass of Model, or string)')

        # Parse keyword parameters
        if model:
            self.model = model

        if uri:
            self.uri = urlparse(uri)

        # Instance properties
        self.items = {}

        # Load collection (if model provided)
        if load and self.model and not self.load():
            log.warn("Unable to load collection for '%s'" % (self.model.__name__,))

    @property
    def internal(self):
        """Retrieve internal model metadata."""
        if not self.model:
            return None

        return self.model.Internal

    @property
    def properties(self):
        """Retrieve model properties."""
        if not self.model:
            return None

        return self.model.Properties

    def bind(self, model):
        """
        Bind collection to data model.

        :param model: Data model
        :type model: byte.model.Model
        """
        if not model or not issubclass(model, Model):
            raise CollectionModelError('Invalid value provided for the "model" parameter (expected Model subclass)')

        self.model = model

        # Load collection
        if self.model and not self.load():
            log.warn("Unable to load collection for '%s'" % (self.model.__name__,))

    def import_items(self, values, generator=False, translate=False):
        """
        Import dictionary of items into collection.

        :param values: Items
        :type values: dict or list or tuple

        :param generator: Enable item import generator (otherwise return list)
        :type generator: bool

        :param translate: Enable item property value translation
        :type translate: bool

        :return: Keys of imported items
        :rtype: generator or list
        """
        if not values:
            return

        # Ensure primary key exists
        if not self.internal.primary_key:
            raise CollectionModelError('Model has no primary key')

        # Resolve `values` parameter
        if type(values) is dict:
            values = values.values()

        # Import items
        def run():
            for value in values:
                pk, item = self.import_item(
                    value,
                    translate=translate
                )

                if not pk:
                    continue

                yield pk

        # Return generator (if enabled), or resolved list
        if generator:
            return run()

        return list(run())

    def import_item(self, value, translate=False):
        """
        Import item into collection.

        :param value: Item Value
        :type value: dict

        :param translate: Enable item property value translation
        :type translate: bool

        :return: `True` if item was imported, `False` if the item couldn't be
                 imported or has already been imported.
        :rtype: bool
        """
        # Parse item from plain dictionary
        item = self.model.from_plain(
            value,
            translate=translate
        )

        if not item:
            raise CollectionParseError('No item could be decoded')

        # Ensure primary key exists
        if not self.internal.primary_key:
            raise CollectionModelError('Model has no primary key')

        # Retrieve primary key
        pk = self.internal.primary_key.get(item)

        if pk is None:
            raise CollectionParseError('Invalid value for primary key: %r' % (pk,))

        # Store item in collection
        self.items[pk] = item

        return pk, item

    def load(self):
        """Reload collection."""
        return False

    def save(self):
        """Save collection."""
        return False

    # region Collection methods

    def get(self, *args, **kwargs):
        """
        Retrieve object matching the provided parameters.

        :param args: Primary key
        :type args: tuple

        :param kwargs: Item parameters
        :type kwargs: dict

        :return: Item
        :rtype: byte.model.Model
        """
        if args:
            if len(args) != 1:
                raise ValueError('Only one positional argument is permitted')

            if kwargs:
                raise ValueError('Positional and keyword arguments can\'t be mixed')

            return self.items.get(args[0])

        raise NotImplementedError

    def get_or_create(self, defaults=None, **kwargs):
        """Try retrieve object matching the provided parameters, create the object if it doesn't exist."""
        raise NotImplementedError

    def create(self, **kwargs):
        """
        Create an object with the provided parameters, and save it to the collection.

        :param kwargs: Item parameters
        :type kwargs: dict
        """
        obj = self.model(_collection=self, **kwargs)
        obj.save()

        return obj

    def insert(self, obj):
        """
        Insert item into the collection.

        :param obj: Instance
        :type obj: byte.model.Model

        :return: Inserted instance
        :rtype: byte.model.Model
        """
        if not isinstance(obj, self.model):
            raise CollectionValidationError('Invalid object for collection')

        if not self.internal.primary_key:
            raise CollectionModelError('Model has no primary key')

        # Retrieve primary key
        key = self.internal.primary_key.get(obj)

        if key is None:
            raise CollectionValidationError('Invalid value for primary key: %r' % (key,))

        # Ensure `key` isn't already in use
        if key in self.items:
            raise KeyError("Key '%s' is already is use" % (key,))

        # Insert item
        self.items[key] = obj

        # Save collection
        self.save()

        return obj

    def bulk_insert(self, objs, batch_size=None):
        """
        Insert multiple items in an efficient manner (usually only one query).

        :param objs: Items
        :type objs: list of byte.model.Model

        :param batch_size: Query batch size
        :type batch_size: int
        """
        raise NotImplementedError

    def update_or_create(self, defaults=None, **kwargs):
        """
        Update object with the given parameters, create an object if it doesn't exist.

        :param defaults: Item defaults
        :type defaults: dict

        :param kwargs: Item parameters
        :type kwargs: dict
        """
        raise NotImplementedError

    def count(self):
        """Retrieve number of currently stored items."""
        raise NotImplementedError

    def iterator(self):
        """Retrieve iterator which yields all currently stored items."""
        raise NotImplementedError

    def latest(self, field_name=None):
        """Retrieve the latest item (by the provided date `field_name`)."""
        raise NotImplementedError

    def oldest(self, field_name=None):
        """Retrieve the oldest item (by the provided date `field_name`)."""
        raise NotImplementedError

    def first(self):
        """Retrieve the first item, or `None` if there is no items."""
        raise NotImplementedError

    def last(self):
        """Retrieve the last item, or `None` if there is no items."""
        raise NotImplementedError

    # endregion


# noinspection PyAbstractClass
class CollectionMixin(Collection):
    """Base class for collection mixins."""
