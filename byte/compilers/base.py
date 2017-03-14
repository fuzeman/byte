class Compiler(object):
    def __init__(self, collection, model):
        self.collection = collection
        self.model = model

    def compile(self, query):
        raise NotImplementedError
