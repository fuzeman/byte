from __future__ import absolute_import, division, print_function

from byte.executors.core.base import FormatExecutorPlugin
from byte.executors.file.revision import FileRevision

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

        # Retrieve directory
        self.directory = os.path.dirname(self.path)

        # Retrieve file extension
        self.name, self.extension = os.path.splitext(self.path)

        if not self.extension:
            raise ValueError('No file extension defined with collection path')

    def construct_format(self):
        return self.plugins.get_collection_format_by_extension(self.extension[1:])()

    def execute(self, statement):
        operation = self.compiler.compile(statement)

        if not operation:
            raise ValueError('Empty statement')

        return self.format.execute(self, operation)

    def read(self):
        return open(self.path)

    def revision(self):
        return FileRevision(self)
