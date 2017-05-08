class Revision(object):
    def __init__(self, executor):
        self.executor = executor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
