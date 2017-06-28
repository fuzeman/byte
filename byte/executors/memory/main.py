"""byte - memory executor module."""

from __future__ import absolute_import, division, print_function

from byte.core.models import InsertOperation, SelectOperation
from byte.core.plugin.base import Plugin
from byte.executors.core.base import SimpleExecutorPlugin
from byte.executors.memory.revision import MemoryRevision
from byte.executors.memory.tasks import MemorySelectTask, MemoryWriteTask


class Base(SimpleExecutorPlugin):
    """Memory base executor class."""

    class Meta(SimpleExecutorPlugin.Meta):
        """Memory base executor metadata."""

        scheme = 'memory'

    def revision(self):
        """Create revision."""
        return MemoryRevision(self)


class MemoryTableExecutor(Base):
    """Memory executor class."""

    key = 'table'

    class Meta(Base.Meta):
        """Memory executor metadata."""

        engine = Plugin.Engine.Table

    def __init__(self, engine, uri, items=None, **kwargs):
        """Create memory executor.

        :param engine: Engine
        :type engine: byte.core.base.datasource.Datasource
        """
        super(MemoryTableExecutor, self).__init__(engine, uri, **kwargs)

        self.items = (
            items
            if items is not None else {}
        )

    def execute(self, query):
        """Execute query.

        :param query: Query
        :type query: byte.queries.Query
        """
        operation = self.compiler.compile(query)

        if not operation:
            raise ValueError('Empty operation')

        if isinstance(operation, InsertOperation):
            return MemoryWriteTask(self, [operation]).execute()

        if isinstance(operation, SelectOperation):
            return MemorySelectTask(self, operation).execute()

        raise NotImplementedError

    def update(self, *args, **kwargs):
        """Update items."""
        self.items.update(*args, **kwargs)


class MemoryDatabaseExecutor(Base):
    """Memory database executor class."""

    key = 'database'

    class Meta(Base.Meta):
        """Memory database executor metadata."""

        engine = Plugin.Engine.Database

    def __init__(self, engine, uri, **kwargs):
        """Create memory database executor.

        :param engine: Database Engine
        :type engine: byte.engines.database.Database

        :param uri: Database URI
        :type uri: ParseResult
        """
        super(MemoryDatabaseExecutor, self).__init__(engine, uri, **kwargs)

        self.tables = {}

    def open_table(self, table):
        """Open memory table executor for :code:`table`.

        :param table: Table
        :type table: byte.engines.table.Table

        :return: Table Executor
        :rtype: MemoryTableExecutor
        """
        if table.name not in self.tables:
            self.tables[table.name] = {}

        return MemoryTableExecutor(
            table, self.uri, self.tables[table.name],
            **self.parameters
        )

    def update(self, *args, **kwargs):
        """Update tables."""
        self.tables.update(*args, **kwargs)
