from byte.core.models import Reader


class CollectionReader(Reader):
    def items(self):
        raise NotImplementedError
