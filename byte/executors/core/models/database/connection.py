from byte.executors.core.models.manager.pool import PoolItem, PoolManager


class DatabaseConnection(PoolItem):
    def __init__(self, executor):
        super(DatabaseConnection, self).__init__()

        self.executor = executor

    def transaction(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.detach()


class DatabaseConnectionPool(PoolManager):
    def __init__(self, executor):
        super(DatabaseConnectionPool, self).__init__()

        self.executor = executor

    def create(self):
        return self.executor.create_connection()
