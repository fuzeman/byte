"""byte - base executor module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types


class Executor(object):
    """Base executor class."""

    def __init__(self, engine, uri, **kwargs):
        """Create executor.

        :param engine: Engine
        :type engine: byte.core.base.engine.Engine

        :param uri: URI
        :type uri: ParseResult
        """
        self.engine = engine

        self.uri = uri
        self.parameters = kwargs

        self._compiler = None

    @property
    def compiler(self):
        """Retrieve current compiler."""
        if not self._compiler:
            self._compiler = self.construct_compiler()

        return self._compiler

    @property
    def plugins(self):
        """Retrieve plugins manager."""
        if not self.engine:
            return None

        return self.engine.plugins

    def construct_compiler(self):
        """Construct compiler."""
        return self.plugins.get('byte.compilers.operation')(self)

    def execute(self, query):
        """Execute query.

        :param query: Query
        :type query: byte.queries.Query
        """
        raise NotImplementedError

    def close(self):
        """Close executor."""
        raise NotImplementedError


class ExecutorPlugin(Executor, Plugin):
    """Base executor plugin class."""

    class Meta(Plugin.Meta):
        """Executor plugin metadata."""

        kind = 'executor'

        content_type = None
        extension = None
        scheme = None

        order_by = Plugin.Meta.order_by + (
            'content_type',
            'extension',
            'scheme'
        )

        @classmethod
        def transform(cls, executor):
            """Transform executor metadata."""
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Default, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Default, value)
            )

            cls.scheme = resolve_tuples(
                cls.scheme,
                lambda value: (Plugin.Priority.Default, value)
            )

        @classmethod
        def validate(cls, executor):
            """Validate executor metadata.

            :param executor: Executor
            :type executor: ExecutorPlugin
            """
            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )

            assert is_list_of(cls.scheme, (int, string_types)), (
                'Invalid value provided for the "scheme" attribute (expected str, [str], [(int, str)])'
            )

            assert len(cls.scheme) > 0, (
                'Invalid value provided for the "scheme" attribute (at least one scheme is required)'
            )
