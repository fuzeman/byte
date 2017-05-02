from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types


class Format(object):
    def encode(self, value, stream):
        raise NotImplementedError

    def decode(self, stream):
        raise NotImplementedError


class FormatPlugin(Format, Plugin):
    key = None
    priority = Plugin.Priority.Medium

    class Meta(Plugin.Meta):
        kind = 'format'
        format_type = None

        content_type = None
        extension = None

        @classmethod
        def transform(cls):
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Medium, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Medium, value)
            )

        @classmethod
        def validate(cls, compiler):
            assert compiler.key, (
                'Plugin has no "key" attribute defined'
            )

            assert isinstance(compiler.key, string_types), (
                'Invalid value provided for the plugin "key" attribute (expected str)'
            )

            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )


class CollectionFormat(Format):
    pass


class CollectionFormatPlugin(CollectionFormat, FormatPlugin):
    format_type = 'collection'


class DocumentFormat(Format):
    pass


class DocumentFormatPlugin(DocumentFormat, FormatPlugin):
    format_type = 'document'
