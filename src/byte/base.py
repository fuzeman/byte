class BaseExpression(object):
    def execute(self, item):
        raise NotImplementedError


class BaseProperty(object):
    def get(self, obj):
        raise NotImplementedError

    def set(self, obj, value):
        raise NotImplementedError
