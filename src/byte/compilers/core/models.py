class Operation(object):
    def __init__(self, compiler, statement):
        self.compiler = compiler
        self.statement = statement

    @property
    def executor(self):
        if not self.compiler:
            return None

        return self.compiler.executor

    def execute(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
