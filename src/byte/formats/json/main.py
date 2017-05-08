from __future__ import absolute_import, division, print_function

from byte.formats.core.base import CollectionFormatPlugin, DocumentFormatPlugin, Format
from byte.formats.json.tasks import JsonSelectTask, JsonWriteTask


class BaseJsonFormat(Format):
    pass


class JsonCollectionFormat(BaseJsonFormat, CollectionFormatPlugin):
    key = 'json:collection'

    class Meta(CollectionFormatPlugin.Meta):
        content_type = 'application/json'
        extension = 'json'

    def insert(self, executor, operation):
        return JsonWriteTask(executor, [operation]).execute()

    def select(self, executor, operation):
        return JsonSelectTask(executor, operation).execute()


class JsonDocumentFormat(DocumentFormatPlugin):
    key = 'json:document'

    class Meta(DocumentFormatPlugin.Meta):
        content_type = 'application/json'
        extension = 'json'
