from byte.executors.core.base.simple import SimpleExecutor, SimpleExecutorPlugin


class FormatExecutor(SimpleExecutor):
    def __init__(self, collection, model):
        super(FormatExecutor, self).__init__(collection, model)

        self._format = None

    @property
    def format(self):
        if not self._format:
            self._format = self.construct_format()

        return self._format

    def construct_format(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError


class FormatExecutorPlugin(FormatExecutor, SimpleExecutorPlugin):
    pass
