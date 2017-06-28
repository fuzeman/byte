"""byte - file executor module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.uri import parse_uri, uri_from_path
from byte.core.plugin.base import Plugin
from byte.executors.core.base import FormatExecutorPlugin
from byte.executors.file.revision import FileRevision

import logging
import os
import six

log = logging.getLogger(__name__)


class FileTableExecutor(FormatExecutorPlugin):
    """File collection executor class."""

    key = 'table'

    class Meta(FormatExecutorPlugin.Meta):
        """File collection executor metadata."""

        engine = Plugin.Engine.Table
        scheme = 'file'

    def __init__(self, engine, uri, **kwargs):
        """Create file executor.

        :param engine: Engine
        :type engine: byte.core.base.datasource.Datasource
        """
        super(FileTableExecutor, self).__init__(engine, uri, **kwargs)

        log.debug('Constructed (engine: table, uri: %r)', self.uri)

        # Retrieve path
        self.path = os.path.abspath(self.uri.netloc + self.uri.path)

        if not self.path:
            raise ValueError('Invalid collection path')

        log.debug(' - path: %r', self.path)

        # Retrieve directory
        self.directory = os.path.dirname(self.path)

        log.debug(' - directory: %r', self.directory)

        # Retrieve file extension
        self.name, self.extension = os.path.splitext(self.path)

        if not self.extension:
            raise ValueError('No file extension defined with collection path')

        log.debug(' - name: %r', self.name)
        log.debug(' - extension: %r', self.extension)

    def construct_format(self):
        """Construct format parser."""
        return self.plugins.match(
            Plugin.Kind.Format,
            engine=Plugin.Engine.Collection,  # Use current engine
            extension=self.extension[1:]
        )()

    def execute(self, query):
        """Execute query.

        :param query: Query
        :type query: byte.queries.Query
        """
        operation = self.compiler.compile(query)

        if not operation:
            raise ValueError('Empty operation')

        return self.format.execute(self, operation)

    def read(self):
        """Open file read stream.

        :return: Stream
        :rtype: file or io.IOBase
        """
        log.debug('Opening file: %s', self.path)

        # Open file stream
        if six.PY2:
            fp = open(self.path)
        else:
            fp = open(self.path, encoding='utf8')

        log.debug('Opened file (fp: %r)', fp)
        return fp

    def revision(self):
        """Create revision."""
        return FileRevision(self)


class FileDatabaseExecutor(FormatExecutorPlugin):
    """File database executor class."""

    key = 'database'

    class Meta(FormatExecutorPlugin.Meta):
        """File database executor metadata."""

        engine = Plugin.Engine.Database
        scheme = 'file'

    def __init__(self, engine, uri, **kwargs):
        super(FileDatabaseExecutor, self).__init__(engine, uri, **kwargs)

        log.debug('Constructed (engine: database, uri: %r)', self.uri)

        # Retrieve path
        self.path = os.path.abspath(self.uri.netloc + self.uri.path)

        if not self.path:
            raise ValueError('Invalid collection path')

        log.debug(' - path: %r', self.path)

        # Retrieve extension from scheme
        self.extension = self.uri.scheme[self.uri.scheme.find('.'):]

        log.debug(' - extension: %r', self.extension)

    def open_table(self, table):
        uri = uri_from_path(
            os.path.join(self.path, table.name + self.extension),
            scheme=self.uri.scheme
        )

        log.debug('Opening table (uri: %r)', uri)

        return FileTableExecutor(
            table, parse_uri(uri),
            **self.parameters
        )
