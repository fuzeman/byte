"""byte - base format executor module."""

from __future__ import absolute_import, division, print_function

from byte.executors.core.base.simple import SimpleExecutor, SimpleExecutorPlugin


class FormatExecutor(SimpleExecutor):
    """Base format executor class."""

    def __init__(self, engine, uri, **kwargs):
        """Create format executor.

        :param datasource: Datasource
        :type datasource: byte.core.base.datasource.Datasource
        """
        super(FormatExecutor, self).__init__(engine, uri, **kwargs)

        self._format = None

    @property
    def format(self):
        """Retrieve current format parser."""
        if not self._format:
            self._format = self.construct_format()

        return self._format

    def construct_format(self):
        """Construct format parser."""
        raise NotImplementedError

    def read(self):
        """Open file read stream.

        :return: Stream
        :rtype: file or io.IOBase
        """
        raise NotImplementedError


class FormatExecutorPlugin(FormatExecutor, SimpleExecutorPlugin):
    """Base format executor plugin class."""

    pass
