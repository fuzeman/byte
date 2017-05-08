from json import JSONEncoder


class JsonEncoder(object):
    def __init__(self, stream, **kwargs):
        self.stream = stream

        self.encoder = JSONEncoder(**kwargs)

    def write_dict(self, items):
        for chunk in self.encoder.iterencode(DictionaryEmitter(items)):
            self.stream.write(chunk)

    def write_list(self, items):
        raise NotImplementedError


class DictionaryEmitter(dict):
    def __init__(self, items, **kwargs):
        super(DictionaryEmitter, self).__init__(**kwargs)

        self._items = items

    def items(self):
        raise Exception('DictionaryEmitter.items() is not supported')

    def iteritems(self):
        for item in self._items:
            yield item

    def __nonzero__(self):
        return True


class ListEmitter(object):
    pass
