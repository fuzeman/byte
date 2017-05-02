from __future__ import absolute_import, division, print_function

from byte.core.models import Reader
from byte.executors.core.base import FormatExecutorPlugin
from byte.statements.core.models import Result

import logging
import os

log = logging.getLogger(__name__)


class FileExecutor(FormatExecutorPlugin):
    key = 'file'

    class Meta(FormatExecutorPlugin.Meta):
        scheme = 'file'

    def __init__(self, collection, model):
        super(FileExecutor, self).__init__(collection, model)

        # Retrieve path
        self.path = os.path.abspath(self.collection.uri.netloc + self.collection.uri.path)

        if not self.path:
            raise ValueError('Invalid collection path')

        # Retrieve file extension
        _, self.extension = os.path.splitext(self.path)

        if not self.extension:
            raise ValueError('No file extension defined with collection path')

    def construct_format(self):
        return self.plugins.get_collection_format_by_extension(self.extension[1:])()

    def execute(self, statement):
        operation = self.compiler.compile(statement)

        if not operation:
            raise ValueError('Empty statement')

        try:
            return FileResult(self.collection, self.model, operation)
        except Exception as ex:
            raise NotImplementedError

    def items(self):
        return FileReader(self)


class FileReader(Reader):
    def __init__(self, executor):
        super(FileReader, self).__init__()

        self.executor = executor

        # Open file stream
        self._stream = open(self.executor.path)

        # Create decoder
        self._decoder = self.format.decode(self._stream)

    @property
    def closed(self):
        return (
            not self._stream or self._stream.closed
        ) and (
            not self._decoder or self._decoder.closed
        )

    @property
    def format(self):
        if not self.executor:
            raise Exception('No executor available')

        return self.executor.format

    @property
    def model(self):
        if not self.executor:
            raise Exception('No executor available')

        return self.executor.model

    def close(self):
        if not self._stream:
            return

        # Close file stream
        self._stream.close()

        # Close decoder
        self._decoder.close()

    def __iter__(self):
        if self.closed:
            raise Exception('File is closed')

        for item in self._decoder.items():
            yield self.model.from_plain(
                item,
                translate=True
            )

    def __repr__(self):
        return '<FileReader path: %r>' % (self._stream.name,)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close file stream
        self.close()


class FileResult(Result):
    def __init__(self, collection, model, operation):
        super(FileResult, self).__init__(collection, model)

        self.operation = operation

    def iterator(self):
        for item in self.operation.execute():
            yield item

    def close(self):
        self.operation.close()
