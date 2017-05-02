import functools


class Statement(object):
    def __init__(self, collection, model, state=None):
        self.collection = collection
        self.model = model

        self.state = state or {}

        self._result = None

    def clone(self):
        def copy(value):
            if type(value) is dict:
                return value.copy()

            if type(value) is list:
                return list(value)

            if type(value) is tuple:
                return tuple(value)

            return value

        return self.__class__(
            self.collection, self.model,
            state=copy(self.state)
        )

    def execute(self):
        return self.collection.execute(self)

    def filter(self, *args, **kwargs):
        raise NotImplementedError

    def first(self):
        with self.execute() as result:
            for item in result:
                return item

        return None

    def __enter__(self):
        self._result = self.execute()

        return self._result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._result is None:
            return

        self._result.close()


def operation(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        if not hasattr(self, 'clone'):
            raise ValueError('Class \'%s\' has no "clone" method defined' % (self.__class__.__name__,))

        # Clone existing query
        query = self.clone()

        # Execute operation, and return new query
        func(query, *args, **kwargs)
        return query

    return inner
