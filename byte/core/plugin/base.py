"""byte - base plugin module."""

from __future__ import absolute_import, division, print_function


class PluginEngines(object):
    """Plugin engines."""

    Any        = 'any'  # noqa
    Database   = 'database'  # noqa

    Table      = 'table'  # noqa

    Collection = 'collection'  # noqa
    Document   = 'document'  # noqa


class PluginKinds(object):
    """Plugin kinds."""

    Compiler = 'compiler'  # noqa
    Executor = 'executor'  # noqa
    Format   = 'format'  # noqa


class PluginPriorities(object):
    """Plugin priorities."""

    Default =     0  # noqa
    Low     =  1000  # noqa
    High    = -1000  # noqa


class Plugin(object):
    """Base plugin class."""

    Engine = PluginEngines
    Kind = PluginKinds
    Priority = PluginPriorities

    key = None
    priority = PluginPriorities.Default

    class Meta(object):
        """Plugin metadata."""

        engine = PluginEngines.Any

        kind = None
        order_by = tuple()

        @classmethod
        def transform(cls, plugin):
            """Transform metadata."""
            pass

        @classmethod
        def validate(cls, plugin):
            """Validate metadata.

            :param plugin: Plugin
            :type plugin: Plugin
            """
            return True
