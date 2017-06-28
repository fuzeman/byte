"""byte - collection module."""
from __future__ import absolute_import, division, print_function

from byte.core.helpers.uri import parse_uri, parse_query
from byte.core.model import Model
from byte.core.plugin.base import Plugin
from byte.engines.core.base import Engine
from byte.queries import DeleteQuery, InsertQuery, SelectQuery, UpdateQuery

from six import string_types
import logging

log = logging.getLogger(__name__)


class TableError(Exception):
    """Collection error class."""
    pass


class Table(Engine):
    """Collection class."""

    def __init__(self, uri_or_model=None, uri=None, model=None, name=None, plugins=None, **kwargs):
        """Create collection.

        :param uri_or_model: Collection URI, or Model
        :type uri_or_model: str or type or None

        :param database: Database, or Collection URI
        :type database: Database or str or None

        :param model: Model
        :type model: class or None

        :param name: Name
        :type name: str or None

        :param plugins: List of plugin modules that should be loaded (or :code:`None` to load all plugin modules)
        :type plugins: list or None
        """
        super(Table, self).__init__(
            plugins=plugins
        )

        self.name = name

        self.relations = {}

        self._database = None
        self._executor = None
        self._model = None

        self._uri = None
        self._parameters = None

        # Resolve dynamic `datasource_or_model` parameter
        if isinstance(uri_or_model, string_types):
            uri = uri_or_model
        elif issubclass(uri_or_model, Model):
            model = uri_or_model
        elif uri_or_model:
            raise ValueError('Invalid value provided for the "datasource_or_model" parameter')

        # Set table model
        self._model = model

        # Parse URI
        if uri:
            self._uri = parse_uri(uri)
            self._parameters = parse_query(self.uri.query)

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        self._database = value

    @property
    def executor(self):
        if not self._executor:
            return self._construct_executor()

        return self._executor

    @executor.setter
    def executor(self, value):
        self._executor = value

    @property
    def internal(self):
        """Retrieve internal model metadata."""
        if not self._model:
            return None

        return self._model.Internal

    @property
    def model(self):
        return self._model

    @property
    def properties(self):
        """Retrieve model properties."""
        if not self._model:
            return None

        return self._model.Properties

    @property
    def uri(self):
        return self._uri

    def connect(self, **kwargs):
        """Connect relation properties to collections."""
        self.relations.update(kwargs)

    def transaction(self):
        """Create transaction.

        :return: Transaction
        :rtype: byte.executors.core.models.database.transaction.DatabaseTransaction
        """
        if not self.executor:
            raise Exception('No executor available')

        transaction = self.executor.transaction()

        if transaction.operations > 0:
            raise Exception('Transaction is already active')

        return transaction

    def execute(self, query):
        """Execute query.

        :param query: Query
        :type query: byte.queries.Query
        """
        if not self.executor:
            raise Exception('No executor available')

        return self.executor.execute(query)

    def all(self):
        """Retrieve all items from collection."""
        return self.select()

    def delete(self):
        """Create delete query."""
        return DeleteQuery(self, self.model)

    def select(self, *properties):
        """Create select query."""
        return SelectQuery(
            self, self.model,
            properties=properties or None
        )

    def update(self, args, **kwargs):
        """Create update query."""
        data = kwargs

        for value in args:
            data.update(value)

        return UpdateQuery(
            self, self.model,
            data=data
        )

    def create(self, **kwargs):
        """Create item."""
        if not self.model:
            raise Exception('Table has no \'model\' defined')

        return self.model.create(
            byte_engine=self,
            **kwargs
        )

    def create_or_get(self):
        """Create (or retrieve the existing) item."""
        raise NotImplementedError

    # TODO Better handling of primary key queries (string values are currently parsed as expressions)
    def get(self, *expressions, **kwargs):
        """Retrieve item."""
        query = self.select().limit(1)

        if expressions:
            query = query.where(*expressions)

        if kwargs:
            query = query.filter(**kwargs)

        return query.first()

    def get_or_create(self):
        """Retrieve existing (or create) item."""
        raise NotImplementedError

    def insert(self, *args):
        """Create insert query."""
        return InsertQuery(
            self, self.model,
            properties=args or None
        )

    def insert_from(self, query, properties):
        """Create insert from query."""
        return InsertQuery(
            self, self.model,
            query=query,
            properties=properties
        )

    def insert_many(self, items):
        """Create insert many query."""
        return InsertQuery(
            self, self.model,
            items=items
        )

    #
    # Private methods
    #

    def _construct_executor(self):
        if not self.uri:
            return None

        # Find collection executor
        cls = self.plugins.match(
            Plugin.Kind.Executor,
            engine=Plugin.Engine.Table,
            scheme=self.uri.scheme
        )

        if not cls:
            return None

        # Construct executor
        self._executor = cls(self, self.uri, **self._parameters)
        return self._executor

    def __repr__(self):
        if self.database and self.model:
            return '<Table \'%s\' of %r in %r>' % (
                self.name,
                self.model,
                self.database
            )

        if self.database:
            return '<Table \'%s\' in %r>' % (
                self.name,
                self.database
            )

        if self.model:
            return '<Table \'%s\' of %r>' % (
                self.name,
                self.model
            )

        return '<Table \'%s\'>' % (
            self.name,
        )


# noinspection PyAbstractClass
class TableMixin(Table):
    """Base class for collection mixins."""
