"""byte - memory executor module."""

from __future__ import absolute_import, division, print_function

from byte.core.models import InsertOperation, SelectOperation
from byte.core.plugin.base import Plugin
from byte.executors.core.base import SimpleExecutorPlugin
from byte.executors.memory.revision import MemoryRevision
from byte.executors.memory.tasks import MemorySelectTask, MemoryWriteTask


class MemoryTableExecutor(SimpleExecutorPlugin):
    """Memory executor class."""

    key = 'table'

    class Meta(SimpleExecutorPlugin.Meta):
        """Memory executor metadata."""

        engine = Plugin.Engine.Table
        scheme = 'memory'

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

    def revision(self):
        """Create revision."""
        return MemoryRevision(self)

    def update(self, *args, **kwargs):
        """Update items."""
        self.items.update(*args, **kwargs)


class MemoryDatabaseExecutor(SimpleExecutorPlugin):
    """Memory database executor class."""

    key = 'database'

    class Meta(SimpleExecutorPlugin.Meta):
        """Memory database executor metadata."""

        engine = Plugin.Engine.Database
        scheme = 'memory'

    def __init__(self, engine, uri, **kwargs):
        super(MemoryDatabaseExecutor, self).__init__(engine, uri, **kwargs)

        self.tables = {}

    def create(self, engine, item):
        if engine == Plugin.Engine.Table:
            return self.create_table(item)

        raise ValueError('Unsupported engine: %s'  % (engine,))

    def create_table(self, table):
        if table.name not in self.tables:
            self.tables[table.name] = {}

        return MemoryTableExecutor(
            table, self.uri, self.tables[table.name],
            **self.parameters
        )
