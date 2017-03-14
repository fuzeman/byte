class Executor(object):
    format = None

    def __init__(self, collection, model):
        self.collection = collection
        self.model = model

    def execute(self, query):
        raise NotImplementedError
