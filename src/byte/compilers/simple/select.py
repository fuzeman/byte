from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import Compiler
from byte.compilers.core.models import Operation

from six import itervalues


class SimpleSelectCompiler(Compiler):
    def __init__(self, parent, executor):
        super(SimpleSelectCompiler, self).__init__(executor)

        self.parent = parent

    def compile(self, statement):
        return SimpleSelectOperation(self, statement)


class SimpleSelectOperation(Operation):
    def __init__(self, compiler, statement):
        super(SimpleSelectOperation, self).__init__(compiler, statement)

        self.items = None

    def execute(self):
        if not self.executor:
            raise Exception('Executor is not available')

        # Retrieve items
        self.items = self.executor.items()

        # Return matching items
        return self._filter(
            self.items,
            self.statement.state.get('where', [])
        )

    def close(self):
        if not self.items:
            return

        self.items.close()

    def _filter(self, items, expressions):
        if isinstance(items, dict):
            items = itervalues(items)

        for item in items:
            if not self._match(item, expressions):
                continue

            yield item

    @staticmethod
    def _match(item, expressions):
        for expression in expressions:
            if not expression.execute(item):
                return False

        return True
