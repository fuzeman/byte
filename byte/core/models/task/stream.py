"""Stream task module."""

from __future__ import absolute_import, division, print_function

from byte.core.models.task.base import Task
from byte.core.models.task.simple import SimpleTask, SimpleReadTask, SimpleSelectTask, SimpleWriteTask


class StreamTask(SimpleTask):
    def __init__(self, executor):
        super(StreamTask, self).__init__(executor)

        self.stream = None

    @property
    def state(self):
        if self.stream is None:
            return Task.State.created

        if self.stream.closed:
            return Task.State.closed

        return Task.State.started

    def open(self):
        if self.closed:
            raise ValueError('Task has been closed')

        if self.started:
            raise ValueError('Task has already been started')

        # Open read stream
        self.stream = self.executor.read()

    def close(self):
        if self.closed:
            raise ValueError('Task has already been closed')

        if not self.started:
            return False

        # Close read stream
        if self.stream:
            self.stream.close()

        return True


class StreamReadTask(SimpleReadTask, StreamTask):
    pass


class StreamSelectTask(SimpleSelectTask, StreamTask):
    pass


class StreamWriteTask(SimpleWriteTask, StreamTask):
    pass
