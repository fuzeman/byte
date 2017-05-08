from byte.compilers.core.models import DeleteOperation, InsertOperation, SelectOperation, UpdateOperation
from byte.core.models import Reader
from byte.formats.core.base.format import Format, FormatPlugin

__all__ = (
    'CollectionFormat',
    'CollectionFormatPlugin',
    'CollectionReader'
)


class CollectionFormat(Format):
    def execute(self, executor, operation):
        if isinstance(operation, DeleteOperation):
            return self.delete(executor, operation)

        if isinstance(operation, InsertOperation):
            return self.insert(executor, operation)

        if isinstance(operation, SelectOperation):
            return self.select(executor, operation)

        if isinstance(operation, UpdateOperation):
            return self.update(executor, operation)

        raise NotImplementedError('Unsupported operation: %s' % (operation,))

    def delete(self, executor, operation):
        raise NotImplementedError('Delete operation hasn\'t been implemented')

    def insert(self, executor, operation):
        raise NotImplementedError('Insert operation hasn\'t been implemented')

    def select(self, executor, operation):
        raise NotImplementedError('Select operation hasn\'t been implemented')

    def update(self, executor, operation):
        raise NotImplementedError('Update operation hasn\'t been implemented')


class CollectionFormatPlugin(CollectionFormat, FormatPlugin):
    format_type = 'collection'


class CollectionReader(Reader):
    def items(self):
        raise NotImplementedError
