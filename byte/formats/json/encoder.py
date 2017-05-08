from json import JSONEncoder
import six


class JsonEncoder(object):
    def __init__(self, stream, **kwargs):
        self.stream = stream

        self.encoder = JSONEncoder(**kwargs)

    def write_dict(self, items):
        for chunk in self.encoder.iterencode(DictionaryEmitter(items)):
            if six.PY3:
                chunk = bytes(chunk, encoding='utf8')

            self.stream.write(chunk)

    def write_list(self, items):
        raise NotImplementedError


class DictionaryEmitter(dict):
    def __init__(self, items):
        super(DictionaryEmitter, self).__init__()

        self._items = items

    def items(self):
        if six.PY2:
            raise Exception('DictionaryEmitter.items() is not supported')

        return self.iteritems()

    def iteritems(self):
        for item in self._items:
            yield item

    def __bool__(self):
        return True

    def __nonzero__(self):
        return True

    def __repr__(self):
        return 'DictionaryEmitter(%r)' % (self._items,)


class ListEmitter(object):
    pass
