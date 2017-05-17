from byte.core.models.threading.pool import PoolItem, PoolManager

from threading import RLock

try:
    from thread import get_ident
except ImportError:
    from threading import get_ident


class DatabaseConnection(PoolItem):
    def __init__(self, executor):
        """Create database connection.
        
        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(DatabaseConnection, self).__init__()

        self.executor = executor

        self._operations = 0
        self._operation_lock = RLock()

    #
    # Properties
    #

    @property
    def operations(self):
        return self._operations

    #
    # Public methods
    #

    def acquire(self):
        """Acquire connection operation lock."""
        if get_ident() != self._ident:
            raise Exception('Connection is in use by another thread')

        with self._operation_lock:
            self._operations += 1

    def release(self):
        """Release connection operation lock."""
        if get_ident() != self._ident:
            raise Exception('Connection is in use by another thread')

        with self._operation_lock:
            self._operations -= 1

            # Detach connection when there are no active operations
            if self._operations < 1:
                self.detach()

    #
    # Abstract methods
    #

    def cursor(self):
        """Create cursor.
        
        :return: Cursor
        :rtype: byte.executors.core.models.database.cursor.DatabaseCursor
        """
        raise NotImplementedError

    def execute(self, *args, **kwargs):
        """Execute statement, and return the cursor.
        
        :return: Cursor
        :rtype: byte.executors.core.models.database.cursor.DatabaseCursor
        """
        raise NotImplementedError

    def transaction(self):
        """Create transaction.
        
        :return: Transaction
        :rtype: byte.executors.core.models.database.transaction.DatabaseTransaction
        """
        raise NotImplementedError

    def close(self):
        """Close connection, and remove it from the pool."""
        raise NotImplementedError

    #
    # Magic methods
    #

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Detach connection
        self.detach()


class DatabaseConnectionPool(PoolManager):
    def __init__(self, executor):
        """Create database connection pool.
        
        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(DatabaseConnectionPool, self).__init__()

        self.executor = executor

    def create(self):
        """Create connection.
        
        ;return: Connection
        :rtype: DatabaseConnection
        """
        return self.executor.create_connection()
