__all__ = (
    'Task',
    'ReadTask',
    'WriteTask'
)


class Task(object):
    class State(object):
        created = 0
        started = 1
        closed  = 2

    def __init__(self, executor):
        self.executor = executor

    @property
    def closed(self):
        return self.state == Task.State.closed

    @property
    def collection(self):
        return self.executor.collection

    @property
    def model(self):
        return self.executor.model

    @property
    def started(self):
        return self.state == Task.State.started

    @property
    def state(self):
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class ReadTask(Task):
    def __init__(self, executor, operation):
        super(ReadTask, self).__init__(executor)

        self.operation = operation


class SelectTask(ReadTask):
    def items(self):
        raise NotImplementedError

    def __iter__(self):
        return iter(self.items())


class WriteTask(Task):
    def __init__(self, executor, operations):
        super(WriteTask, self).__init__(executor)

        self.operations = operations
