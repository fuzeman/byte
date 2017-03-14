from byte.executors.base import Executor
from byte.statements import InsertStatement, SelectStatement, StatementResult

from six import iteritems


class MemoryExecutor(Executor):
    def __init__(self, collection, model):
        super(MemoryExecutor, self).__init__(collection, model)

        self.items = {}

    def execute(self, statement):
        if isinstance(statement, InsertStatement):
            return self.execute_insert(statement)

        if isinstance(statement, SelectStatement):
            return self.execute_select(statement)

        raise NotImplementedError

    def execute_insert(self, statement):
        primary_key = self.model.Internal.primary_key

        if not primary_key:
            raise Exception('No primary key available')

        # Insert items
        for x, item in enumerate(statement.items):
            key = primary_key.get(item)

            if key is None:
                raise Exception('No primary key defined for item #%d' % (x,))

            if key in self.items:
                raise Exception('Item with key %r already exists' % (key,))

            self.items[key] = item

        return True

    def execute_select(self, statement):
        return MemoryStatementResult(
            self.collection, self.model,
            self.__filter_items(self.items, statement.state.get('where', []))
        )

    def __filter_items(self, items, expressions):
        for _, item in iteritems(items):
            if not self.__validate(item, expressions):
                continue

            yield item

    def __validate(self, item, expressions):
        for expression in expressions:
            if not expression.execute(item):
                return False

        return True


class MemoryStatementResult(StatementResult):
    def __init__(self, collection, model, items):
        super(MemoryStatementResult, self).__init__(collection, model)

        self.items = items

    def iterator(self):
        for item in self.items:
            yield self.model.from_plain(
                item,
                translate=True
            )
