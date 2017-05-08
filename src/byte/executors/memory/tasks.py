from byte.core.models import Task, SimpleTask, SimpleReadTask, SimpleSelectTask, SimpleWriteTask

import six


class MemoryTask(SimpleTask):
    def __init__(self, executor):
        super(MemoryTask, self).__init__(executor)

        self._state = Task.State.created

    @property
    def state(self):
        return self._state

    def open(self):
        # Update state
        self._state = Task.State.started

    def close(self):
        # Update state
        self._state = Task.State.closed

        return True


class MemoryReadTask(SimpleReadTask, MemoryTask):
    pass


class MemorySelectTask(SimpleSelectTask, MemoryReadTask):
    def decode(self):
        return six.itervalues(self.executor.items)


class MemoryWriteTask(SimpleWriteTask, MemoryTask):
    def decode(self):
        return six.itervalues(self.executor.items)

    def encode(self, revision, items):
        revision.items.update(items)
