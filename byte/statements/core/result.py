class StatementResult(object):
    def __init__(self, collection, model):
        self.collection = collection
        self.model = model

    def count(self):
        raise NotImplementedError

    def iterator(self):
        raise NotImplementedError

    def __iter__(self):
        return iter(self.iterator())

    def __len__(self):
        return self.count()
