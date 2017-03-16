from __future__ import absolute_import, division, print_function

from byte.executors.core.base import ExecutorPlugin
from byte.compilers.core.base import Compiler
from byte.statements.core.result import StatementResult

import inspect
import os


class FileExecutor(ExecutorPlugin):
    key = 'file'

    class Meta(ExecutorPlugin.Meta):
        scheme = 'file'

    def __init__(self, collection, model):
        super(FileExecutor, self).__init__(collection, model)

        self._compiler = None

        # Retrieve path
        self.path = os.path.join(self.collection.uri.netloc, self.collection.uri.path)

        if not self.path:
            raise ValueError('Invalid collection path')

        # Retrieve file extension
        _, self.extension = os.path.splitext(self.path)

        if not self.extension:
            raise ValueError('No file extension defined with collection path')

    @property
    def compiler(self):
        if not self._compiler:
            self._compiler = self._get_compiler(self.extension[1:])(self)

        return self._compiler

    def execute(self, statement):
        operation = self.compiler.compile(statement)

        if not operation:
            raise ValueError('Empty statement')

        try:
            return FileStatementResult(self.collection, self.model, operation)
        except Exception as ex:
            raise NotImplementedError

    def exists(self):
        return os.path.exists(self.path)

    def read(self):
        return open(self.path)

    def write(self):
        return open(self.path, 'w')

    @staticmethod
    def _get_compiler(key):
        name = 'byte.compilers.%s' % key

        # Import compiler module
        compiler = __import__(name, fromlist=['*'])

        # Find compiler
        for key in dir(compiler):
            if key.startswith('_'):
                continue

            value = getattr(compiler, key)

            if not inspect.isclass(value) or value.__module__ != name:
                continue

            if value is not Compiler and issubclass(value, Compiler):
                return value

        return None


class FileStatementResult(StatementResult):
    def __init__(self, collection, model, operation):
        super(FileStatementResult, self).__init__(collection, model)

        self.operation = operation

    def iterator(self):
        results = self.operation()

        if not results:
            return

        for item in results:
            yield self.model.from_plain(
                item,
                translate=True
            )

    def __iter__(self):
        return self.iterator()
