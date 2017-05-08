import json
import six


class JsonDecoder(object):
    def __init__(self, stream):
        self.stream = stream

    @property
    def closed(self):
        return not self.stream or self.stream.closed

    def items(self):
        data = json.load(self.stream)

        if type(data) is dict:
            return six.itervalues(data)

        if type(data) is list:
            return data

        raise ValueError('Unsupported data type: %s' % (type(data),))

    def close(self):
        if not self.stream or self.stream.closed:
            return

        self.stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
