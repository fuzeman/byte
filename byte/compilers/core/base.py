"""byte - base compiler module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types


class Compiler(object):
    """Base compiler class."""

    def __init__(self, executor):
        """Create compiler.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        self.executor = executor

    @property
    def engine(self):
        """Retrieve engine.

        :return: Engine
        :rtype: byte.table.Table
        """
        if not self.executor:
            return None

        return self.executor.engine

    @property
    def model(self):
        """Retrieve model.

        :return: Model
        :rtype: byte.model.Model
        """
        if not self.executor:
            return None

        return self.executor.model

    def compile(self, query):
        """Compile query.

        :param query: Query
        :type query: byte.queries.Query
        """
        raise NotImplementedError


class CompilerPlugin(Compiler, Plugin):
    """Base compiler plugin class."""

    class Meta(Plugin.Meta):
        """Compiler metadata."""

        kind = 'compiler'

        content_type = None
        extension = None

        order_by = (
            'content_type',
            'extension'
        )

        @classmethod
        def transform(cls, compiler):
            """Transform compiler metadata."""
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Default, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Default, value)
            )

        @classmethod
        def validate(cls, compiler):
            """Validate compiler metadata.

            :param compiler: Compiler
            :type compiler: Compiler
            """
            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )
