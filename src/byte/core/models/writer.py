class Writer(object):
    @property
    def closed(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
