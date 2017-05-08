from __future__ import absolute_import, division, print_function

from byte.executors.core.base import SimpleExecutorPlugin
from byte.compilers.core.models import InsertOperation, SelectOperation
from byte.executors.memory.revision import MemoryRevision
from byte.executors.memory.tasks import MemorySelectTask, MemoryWriteTask


class MemoryExecutor(SimpleExecutorPlugin):
    key = 'memory'

    class Meta(SimpleExecutorPlugin.Meta):
        scheme = 'memory'

    def __init__(self, collection, model):
        super(MemoryExecutor, self).__init__(collection, model)

        self.items = {}

    def execute(self, statement):
        operation = self.compiler.compile(statement)

        if not operation:
            raise ValueError('Empty statement')

        if isinstance(operation, InsertOperation):
            return MemoryWriteTask(self, [operation]).execute()

        if isinstance(operation, SelectOperation):
            return MemorySelectTask(self, operation).execute()

        raise NotImplementedError

    def revision(self):
        return MemoryRevision(self)

    def update(self, *args, **kwargs):
        self.items.update(*args, **kwargs)
