from __future__ import absolute_import, division, print_function

from byte.core.models import Reader
from byte.executors.core.base import SimpleExecutorPlugin
from byte.statements import Result


class MemoryExecutor(SimpleExecutorPlugin):
    key = 'memory'

    class Meta(SimpleExecutorPlugin.Meta):
        scheme = 'memory'

    def __init__(self, collection, model):
        super(MemoryExecutor, self).__init__(collection, model)

        self._items = {}

    def execute(self, statement):
        operation = self.compiler.compile(statement)

        if not operation:
            raise ValueError('Empty statement')

        return MemoryResult(self.collection, self.model, operation)

    def insert(self, items):
        primary_key = self.model.Internal.primary_key

        if not primary_key:
            raise Exception('No primary key available')

        # Insert items
        for x, item in enumerate(items):
            key = primary_key.get(item)

            if key is None:
                raise Exception('No primary key defined for item #%d' % (x,))

            if key in self._items:
                raise Exception('Item with key %r already exists' % (key,))

            self._items[key] = item

        return True

    def items(self):
        return MemoryReader(self, self._items)

    def update(self, items):
        self._items.update(items)


class MemoryReader(Reader):
    def __init__(self, executor, items):
        super(MemoryReader, self).__init__()

        self.executor = executor

        self._items = items

    @property
    def closed(self):
        return self._items is None

    @property
    def model(self):
        if not self.executor:
            raise Exception('No executor available')

        return self.executor.model

    def close(self):
        self._items = None

    def __iter__(self):
        if self.closed:
            raise Exception('File is closed')

        for item in self._items.values():
            yield self.model.from_plain(
                item,
                translate=True
            )

    def __repr__(self):
        return '<MemoryReader>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close file stream
        self.close()


class MemoryResult(Result):
    def __init__(self, collection, model, operation):
        super(MemoryResult, self).__init__(collection, model)

        self.operation = operation

        self.results = self.operation.execute()

    def iterator(self):
        for item in self.results:
            yield item

    def close(self):
        self.operation.close()
