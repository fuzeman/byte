"""byte - base format module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types

__all__ = (
    'Format',
    'FormatPlugin'
)


class Format(object):
    """Format base class."""

    pass


class FormatPlugin(Format, Plugin):
    """Format plugin class."""

    class Meta(Plugin.Meta):
        """Format metadata."""

        kind = 'format'

        content_type = None
        extension = None

        order_by = Plugin.Meta.order_by + (
            'content_type',
            'extension'
        )

        @classmethod
        def transform(cls, fmt):
            """Transform format metadata."""
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Default, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Default, value)
            )

        @classmethod
        def validate(cls, fmt):
            """Validate format metadata.

            :param fmt: Format
            :type fmt: FormatPlugin
            """
            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )
