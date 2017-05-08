"""Plugin base module."""

from __future__ import absolute_import, division, print_function


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
        Low     =  1000  # noqa
        Medium  =     0  # noqa
        High    = -1000  # noqa
