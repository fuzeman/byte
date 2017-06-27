from __future__ import absolute_import, division, print_function

from byte.core.compat import PY26

from six.moves.urllib.parse import ParseResult, parse_qsl, urlparse
from six.moves.urllib.request import pathname2url


def parse_uri(uri):
    if not uri:
        return

    if PY26:
        # Retrieve scheme from `uri`
        scheme_end = uri.index('://')
        scheme = uri[0:scheme_end]

        # Replace scheme in `uri` with "http" (to avoid parsing bugs)
        uri = 'http' + uri[scheme_end:]

        # Parse URI
        parsed = urlparse(uri)

        # Build parse result with original scheme
        return ParseResult(scheme, *parsed[1:])

    return urlparse(uri)


def parse_query(query):
    if not query:
        return {}

    return dict(parse_qsl(query))


def uri_from_path(path, scheme='file'):
    """Build file URI from path.

    :param path: Path
    :type path: str

    :return: File URI
    :rtype: str
    """
    return scheme + ':' + pathname2url(str(path))[1:]
