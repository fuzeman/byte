from __future__ import absolute_import

from byte.formats.core.base import CollectionFormatPlugin, DocumentFormatPlugin, Format
from byte.formats.core.models import CollectionReader

import json
import six


class BaseJsonFormat(Format):
    def encode(self, value, stream):
        json.dump(value, stream)

    def decode(self, stream):
        return json.load(stream)


class JsonCollectionFormat(BaseJsonFormat, CollectionFormatPlugin):
    key = 'json:collection'

    class Meta(CollectionFormatPlugin.Meta):
        content_type = 'application/json'
        extension = 'json'

    def decode(self, stream):
        return JsonCollectionReader(
            super(JsonCollectionFormat, self).decode(stream)
        )


class JsonCollectionReader(CollectionReader):
    def __init__(self, value):
        super(JsonCollectionReader, self).__init__()

        self._value = value

    @property
    def closed(self):
        return self._value is None

    def items(self):
        if type(self._value) is dict:
            # Yield dictionary item values
            for item in six.itervalues(self._value):
                yield item
        elif type(self._value) is list:
            # Yield list values
            for item in self._value:
                yield item
        else:
            raise ValueError('Unsupported value type')

        # Release resources
        self.close()

    def close(self):
        self._value = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class JsonDocumentFormat(BaseJsonFormat, DocumentFormatPlugin):
    key = 'json:document'

    class Meta(DocumentFormatPlugin.Meta):
        content_type = 'application/json'
        extension = 'json'
