from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import CompilerPlugin
from byte.compilers.simple.insert import SimpleInsertCompiler
from byte.compilers.simple.select import SimpleSelectCompiler
from byte.statements import InsertStatement, SelectStatement


class SimpleCompiler(CompilerPlugin):
    key = 'simple'

    def __init__(self, executor):
        super(SimpleCompiler, self).__init__(executor)

        self.insert = SimpleInsertCompiler(self, executor)
        self.select = SimpleSelectCompiler(self, executor)

    def compile(self, statement):
        if isinstance(statement, InsertStatement):
            return self.insert.compile(statement)

        if isinstance(statement, SelectStatement):
            return self.select.compile(statement)

        raise NotImplementedError
