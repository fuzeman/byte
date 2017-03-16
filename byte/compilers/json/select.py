from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import Compiler

from six import itervalues
import json


class JsonSelectCompiler(Compiler):
    def compile(self, statement):
        return lambda: self.execute(statement)

    def execute(self, statement):
        if not self.executor.exists():
            return None

        with self.executor.read() as stream:
            items = json.load(stream)

        return self.__filter_items(items, statement.state.get('where', []))

    def __filter_items(self, items, expressions):
        if isinstance(items, dict):
            items = itervalues(items)

        for item in items:
            if not self.__validate(item, expressions):
                continue

            yield item

    def __validate(self, item, expressions):
        for expression in expressions:
            if not expression.execute(item):
                return False

        return True
