from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import CompilerPlugin
from byte.compilers.core.models import InsertOperation, SelectOperation
from byte.statements import InsertStatement, SelectStatement


class OperationCompiler(CompilerPlugin):
    key = 'operation'

    def compile(self, statement):
        if isinstance(statement, InsertStatement):
            return self.compile_insert(statement)

        if isinstance(statement, SelectStatement):
            return self.compile_select(statement)

        raise NotImplementedError('Unsupported statement: %s' % (statement,))

    def compile_insert(self, statement):
        if statement.properties:
            raise NotImplementedError('"properties" attribute is not supported on insert statements')

        if statement.query:
            raise NotImplementedError('"query" attribute is not supported on insert statements')

        return InsertOperation(
            items=statement.items
        )

    def compile_select(self, statement):
        return SelectOperation(
            where=statement.state.get('where', [])
        )
