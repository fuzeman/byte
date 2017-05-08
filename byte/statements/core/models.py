class Result(object):
    def __init__(self, collection, model):
        self.collection = collection
        self.model = model

    def close(self):
        raise NotImplementedError

    def count(self):
        raise NotImplementedError

    def iterator(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return iter(self.iterator())

    def __len__(self):
        return self.count()
