from byte.executors.core.models.database.cursor import DatabaseCursor
from byte.core.models.threading.local import LocalItem, LocalManager


class DatabaseTransaction(DatabaseCursor, LocalItem):
    class State(object):
        Created = 0
        Started = 1
        Done = 2

    def __init__(self, executor):
        super(DatabaseTransaction, self).__init__(executor)

        self.state = DatabaseTransaction.State.Created

        self.contexts = 0

    def begin(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def __enter__(self):
        # Begin transaction on the first context
        if self.contexts == 0:
            self.begin()

        self.contexts += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.contexts -= 1

        # Wait for the final context
        if self.contexts > 0:
            return

        # Commit (or rollback) transaction
        if exc_type:
            self.rollback()
        else:
            self.commit()

        # Detach transaction
        self.detach()

        # Close cursor
        self.close()


class DatabaseTransactionManager(LocalManager):
    def __init__(self, executor):
        super(DatabaseTransactionManager, self).__init__()

        self.executor = executor

    def create(self):
        return self.executor.create_transaction()
