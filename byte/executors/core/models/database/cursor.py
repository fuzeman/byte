class DatabaseCursor(object):
    def __init__(self, executor):
        self.executor = executor

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
