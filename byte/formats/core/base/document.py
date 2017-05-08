"""Document format base module."""

from __future__ import absolute_import, division, print_function

from byte.formats.core.base.format import Format, FormatPlugin

__all__ = (
    'DocumentFormat',
    'DocumentFormatPlugin'
)


class DocumentFormat(Format):
    pass


class DocumentFormatPlugin(DocumentFormat, FormatPlugin):
    format_type = 'document'
