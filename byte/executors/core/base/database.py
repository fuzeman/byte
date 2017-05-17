"""Database executor base module."""

from __future__ import absolute_import, division, print_function

from byte.executors.core.base.executor import Executor, ExecutorPlugin
from byte.executors.core.models.database import DatabaseConnectionPool, DatabaseTransactionManager


class DatabaseExecutor(Executor):
    """Base database executor class."""

    def __init__(self, collection, model):
        super(DatabaseExecutor, self).__init__(collection, model)

        self.connections = DatabaseConnectionPool(self)
        self.transactions = DatabaseTransactionManager(self)

    def connection(self, blocking=False):
        """Retrieve current connection."""
        return self.connections.get(
            blocking=blocking
        )

    def transaction(self, **kwargs):
        return self.transactions.get(**kwargs)

    def create_connection(self):
        """Create database connection."""
        raise NotImplementedError

    def create_transaction(self):
        """Create database transaction."""
        raise NotImplementedError


class DatabaseExecutorPlugin(DatabaseExecutor, ExecutorPlugin):
    """Base database executor plugin class."""

    pass
