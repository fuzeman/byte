"""byte - file executor module."""
from __future__ import absolute_import, division, print_function

from byte.core.helpers.uri import parse_uri, path_from_uri, uri_from_path
from byte.core.plugin.base import Plugin
from byte.executors.core.base import FormatExecutorPlugin
from byte.executors.file.revision import FileRevision

import logging
import os
import six

log = logging.getLogger(__name__)


class Base(FormatExecutorPlugin):
    """File base executor class."""

    class Meta(FormatExecutorPlugin.Meta):
        """File base executor metadata."""

        scheme = 'file'

    def __init__(self, engine, uri, **kwargs):
        """Create file executor.

        :param engine: Engine
        :type engine: byte.core.base.datasource.Datasource
        """
        super(Base, self).__init__(engine, uri, **kwargs)

        if self.uri.netloc:
            raise ValueError('Network shares are not supported (invalid uri format)')

        # Retrieve path
        self.path = os.path.abspath(path_from_uri(self.uri.path))

        if not self.path:
            raise ValueError('Invalid collection path')

        # Retrieve directory
        self.directory = os.path.dirname(self.path)

    def construct_format(self):
        """Construct format parser."""
        return self.plugins.match(
            Plugin.Kind.Format,
            engine=Plugin.Engine.Collection,  # Use current engine
            extension=self.extension[1:]
        )(**dict([
            (key.lstrip('format_'), value) for key, value in self.parameters.items()
            if key.startswith('format_')
        ]))

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
        if six.PY2:
            return open(self.path)

        return open(self.path, encoding='utf8')

    def revision(self):
        """Create revision."""
        return FileRevision(self)


class FileTableExecutor(Base):
    """File collection executor class."""

    key = 'table'

    class Meta(Base.Meta):
        """File collection executor metadata."""

        engine = Plugin.Engine.Table

    def __init__(self, engine, uri, **kwargs):
        """Create file executor.

        :param engine: Engine
        :type engine: byte.core.base.datasource.Datasource
        """
        super(FileTableExecutor, self).__init__(engine, uri, **kwargs)

        # Retrieve file extension
        self.name, self.extension = os.path.splitext(self.path)

        if not self.extension:
            raise ValueError('No file extension defined with collection path')


class FileDatabaseExecutor(Base):
    """File database executor class."""

    key = 'database'

    class Meta(Base.Meta):
        """File database executor metadata."""

        engine = Plugin.Engine.Database

    def __init__(self, engine, uri, **kwargs):
        """Create file database executor.

        :param engine: Database Engine
        :type engine: byte.engines.database.Database

        :param uri: Database URI
        :type uri: ParseResult
        """
        super(FileDatabaseExecutor, self).__init__(engine, uri, **kwargs)

        # Retrieve extension from scheme
        self.extension = self.uri.scheme[self.uri.scheme.find('.'):]

    def open_table(self, table):
        """Open file table executor for :code:`table`.

        :param table: Table
        :type table: byte.engines.table.Table

        :return: Table Executor
        :rtype: FileTableExecutor
        """
        uri = uri_from_path(
            os.path.join(self.path, table.name + self.extension),
            scheme=self.uri.scheme
        )

        return FileTableExecutor(
            table, parse_uri(uri),
            **self.parameters
        )
