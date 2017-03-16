from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import CompilerPlugin
from byte.compilers.json.insert import JsonInsertCompiler
from byte.compilers.json.select import JsonSelectCompiler
from byte.statements import InsertStatement, SelectStatement


class JsonCompiler(CompilerPlugin):
    key = 'json'

    class Meta(CompilerPlugin.Meta):
        content_type = 'application/json'
        extension = 'json'

    def __init__(self, executor):
        super(JsonCompiler, self).__init__(executor)

        self.insert = JsonInsertCompiler(executor)
        self.select = JsonSelectCompiler(executor)

    def compile(self, statement):
        if isinstance(statement, InsertStatement):
            return self.insert.compile(statement)

        if isinstance(statement, SelectStatement):
            return self.select.compile(statement)

        raise NotImplementedError
