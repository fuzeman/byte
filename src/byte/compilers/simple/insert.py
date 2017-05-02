from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import Compiler
from byte.compilers.core.models import Operation


class SimpleInsertCompiler(Compiler):
    def __init__(self, parent, executor):
        super(SimpleInsertCompiler, self).__init__(executor)

        self.parent = parent

    def compile(self, statement):
        return SimpleInsertOperation(self, statement)


class SimpleInsertOperation(Operation):
    def execute(self):
        if not self.executor:
            raise Exception('Executor is not available')

        self.executor.insert(self.statement.items)

    def close(self):
        pass
