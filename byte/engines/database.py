"""byte - database module."""
from __future__ import absolute_import, division, print_function

from byte.core.helpers.uri import parse_uri, parse_query
from byte.core.plugin.base import Plugin
from byte.engines.core.base import Engine
from byte.engines.table import Table

import logging
import six

log = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Database error class."""
    pass


class Database(Engine):
    """Database class."""

    def __init__(self, uri, children, **kwargs):
        """Create database.

        :param uri: URI
        :type uri: str

        :param children: Children
        :type children: list
        """
        super(Database, self).__init__(**kwargs)

        self._executor = None

        self._uri = None
        self._parameters = None

        # Parse URI
        if uri:
            self._uri = parse_uri(uri)
            self._parameters = parse_query(self.uri.query)

        # Create collections container
        self.children = DatabaseChildren(children)

        for item in six.itervalues(self.children.by_name):
            # Bind collection to database
            item.database = self

            # Create collection executor
            item.executor = self.executor.create(self.children.engine, item)

    @property
    def executor(self):
        if not self._executor:
            return self._construct_executor()

        return self._executor

    @property
    def uri(self):
        return self._uri

    #
    # Private methods
    #

    def _construct_executor(self):
        if not self.uri:
            return None

        scheme = self.uri.scheme.split('.', 1)[0]

        # Find collection executor
        cls = self.plugins.match(
            Plugin.Kind.Executor,
            engine=Plugin.Engine.Database,
            scheme=scheme
        )

        if not cls:
            return None

        # Construct executor
        self._executor = cls(self, self.uri, **self._parameters)

        return self._executor

    def __getitem__(self, name):
        return self.children.by_name[name]

    def __repr__(self):
        return '<Database \'%s\'>' % (
            self.uri,
        )


class DatabaseChildren(object):
    def __init__(self, children=None):
        self.engine = None

        # Indexes
        self.by_model = {}
        self.by_name = {}

        # Add children
        if children:
            self.add(*children)

    def add(self, *items):
        for item in items:
            engine = self._get_engine(item)

            if item.name is None:
                raise ValueError('Item %r has no "name" defined' % (item,))

            if self.engine and engine != self.engine:
                raise ValueError('Item %r should inherit %s' % (item, self.type.__name__,))

            if item.name in self.by_name:
                raise ValueError('Item with name %r has already been added' % (item.name,))

            # Add to 'name' index
            self.by_name[item.name] = item

            # Add to 'model' index
            if item.model not in self.by_model:
                self.by_model[item.model] = set()

            self.by_model[item.model].add(item)

            # Set child engine
            self.engine = engine

    @staticmethod
    def _get_engine(item):
        if isinstance(item, Table):
            return Plugin.Engine.Table

        raise ValueError('Unknown item type: %s' % (item.__class__.__name__,))
