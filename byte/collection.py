# -*- coding: utf-8 -*-

"""Contains the collection structure for the storage of keyed items."""

from byte.executors.base import Executor
from byte.model import Model
from byte.statements import DeleteStatement, InsertStatement, SelectStatement, UpdateStatement

from six import string_types
from six.moves.urllib.parse import parse_qsl, urlparse
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

    def __init__(self, model_or_uri=None, uri=None, model=None, executor=None):
        """
        Create keyed item collection.

        :param uri: Data Source URI
        :type uri: str

        :param model: Collection data model
        :type model: class
        """
        self.model = None

        self.uri = None
        self.parameters = {}

        self._executor = None
        self._executor_cls = None

        # Parse dynamic parameter
        if model_or_uri:
            if inspect.isclass(model_or_uri) and issubclass(model_or_uri, Model):
                model = model_or_uri
            elif isinstance(model_or_uri, string_types):
                uri = model_or_uri
            else:
                raise ValueError('Unknown initialization parameter value (expected subclass of Model, or string)')

        # Parse keyword parameters
        if model:
            self.model = model

        if uri:
            # Parse Data Source URI
            self.uri = urlparse(uri)

            if self.uri.query:
                self.parameters = dict(parse_qsl(self.uri.query))

            # Find matching executor class
            self._executor_cls = self._get_executor(self.uri.scheme)
        elif executor:
            self._executor_cls = executor

    @property
    def executor(self):
        if not self._executor:
            if not self._executor_cls:
                raise CollectionLoadError('No executor available')

            self._executor = self._executor_cls(
                self,
                self.model
            )

        return self._executor

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

    #region Operations

    def all(self):
        return self.select()

    def delete(self):
        return DeleteStatement(self, self.model)

    def select(self, *properties):
        return SelectStatement(
            self, self.model,
            properties=properties
        )

    def update(self, args, **kwargs):
        data = kwargs

        for value in args:
            data.update(value)

        return UpdateStatement(
            self, self.model,
            data=data
        )

    #region Create

    def create(self, **kwargs):
        if not self.model:
            raise Exception('Collection has no model bound')

        return self.model.create(
            _collection=self,
            **kwargs
        )

    def create_or_get(self):
        raise NotImplementedError

    #endregion

    #region Get

    def get(self, *query, **kwargs):
        statement = self.select().limit(1)

        if query:
            statement = statement.where(*query)

        if kwargs:
            statement = statement.filter(**kwargs)

        return statement.get()

    def get_or_create(self):
        raise NotImplementedError

    #endregion

    #region Insert

    def insert(self, *args, **kwargs):
        item = kwargs

        for value in args:
            item.update(value)

        return InsertStatement(
            self, self.model,
            items=[item]
        )

    def insert_from(self, query, properties):
        return InsertStatement(
            self, self.model,
            query=query,
            properties=properties
        )

    def insert_many(self, items):
        return InsertStatement(
            self, self.model,
            items=items
        )

    #endregion

    #endregion

    def _get_executor(self, key):
        # Import storage package for collection
        storage = __import__('byte.executors.%s' % key, fromlist=['*'])

        # Find executor
        for key in dir(storage):
            if key.startswith('_'):
                continue

            value = getattr(storage, key)

            if not inspect.isclass(value):
                continue

            if value is not Executor and issubclass(value, Executor):
                return value

        return None


# noinspection PyAbstractClass
class CollectionMixin(Collection):
    """Base class for collection mixins."""
