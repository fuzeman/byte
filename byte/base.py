class BaseExpression(object):
    pass


class BaseProperty(object):
    def get(self, obj):
        raise NotImplementedError

    def set(self, obj, value):
        raise NotImplementedError
