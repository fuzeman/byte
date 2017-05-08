from byte.formats.core.base.format import Format, FormatPlugin

__all__ = (
    'DocumentFormat',
    'DocumentFormatPlugin'
)


class DocumentFormat(Format):
    pass


class DocumentFormatPlugin(DocumentFormat, FormatPlugin):
    format_type = 'document'
