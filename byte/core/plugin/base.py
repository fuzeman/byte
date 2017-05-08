class Plugin(object):
    class Meta(object):
        kind = None

        @classmethod
        def transform(cls):
            pass

        @classmethod
        def validate(cls, plugin):
            return True

    class Priority(object):
        Low     =  1000
        Medium  =     0
        High    = -1000
