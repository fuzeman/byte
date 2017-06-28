"""byte - uri helper functions module."""
from __future__ import absolute_import, division, print_function

from byte.core.compat import PY26

from six.moves.urllib.parse import ParseResult, parse_qsl, urlparse
from six.moves.urllib.request import pathname2url, url2pathname


def parse_uri(uri):
    """Parse URI into individual components.

    :param uri: URI
    :type uri: str

    :return: URI Components
    :rtype: ParseResult
    """
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
    """Parse query into dictionary of parameters.

    :param query: Query String
    :type query: str

    :return: Parameters
    :rtype: dict
    """
    if not query:
        return {}

    return dict(parse_qsl(query))


def path_from_uri(uri):
    """Build path from File URI.

    :param uri: File URI
    :type uri: str

    :return: Path
    :rtype: str
    """
    return url2pathname(uri)


def uri_from_path(path, scheme='file'):
    """Build File URI from path.

    :param path: Path
    :type path: str

    :return: File URI
    :rtype: str
    """
    path = pathname2url(str(path))

    if path.startswith('///'):
        path = path[2:]

    return scheme + '://' + path
