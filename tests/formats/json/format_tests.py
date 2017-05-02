from byte.formats.json import JsonCollectionFormat, JsonCollectionReader, JsonDocumentFormat

from six import StringIO


#
# Collections
#

def test_encode_collection():
    fmt = JsonCollectionFormat()
    buf = StringIO()

    fmt.encode([{'label': 'One', 'value': 1}], buf)

    assert buf.getvalue() == '[{"value": 1, "label": "One"}]'


def test_decode_collection():
    fmt = JsonCollectionFormat()
    buf = StringIO('[{"value": 1, "label": "One"}]')

    result = fmt.decode(buf)

    assert isinstance(result, JsonCollectionReader)

    assert list(result.items()) == [
        {'label': 'One', 'value': 1}
    ]

#
# Documents
#

def test_encode_document():
    fmt = JsonDocumentFormat()
    buf = StringIO()

    fmt.encode({'label': 'One', 'value': 1}, buf)

    assert buf.getvalue() == '{"value": 1, "label": "One"}'


def test_decode_document():
    fmt = JsonDocumentFormat()
    buf = StringIO('{"value": 1, "label": "One"}')

    assert fmt.decode(buf) == {'label': 'One', 'value': 1}
