from byte.core.models import StreamTask, StreamReadTask, StreamSelectTask, StreamWriteTask, Task
from byte.formats.json.decoder import JsonDecoder
from byte.formats.json.encoder import JsonEncoder


class JsonTask(StreamTask):
    pass


class JsonReadTask(StreamReadTask, JsonTask):
    def __init__(self, executor, operation):
        super(JsonReadTask, self).__init__(executor, operation)

        self.decoder = None

    @property
    def state(self):
        state = super(JsonReadTask, self).state

        if self.decoder is None or state == Task.State.created:
            return Task.State.created

        if self.decoder.closed or state == Task.State.closed:
            return Task.State.closed

        return Task.State.started

    def open(self):
        super(JsonReadTask, self).open()

        # Create decoder
        self.decoder = JsonDecoder(self.stream)

    def close(self):
        if not super(JsonReadTask, self).close():
            return False

        # Close decoder
        if self.decoder:
            self.decoder.close()

        return True


class JsonSelectTask(StreamSelectTask, JsonReadTask):
    def decode(self):
        return self.decoder.items()


class JsonWriteTask(StreamWriteTask, JsonTask):
    def __init__(self, executor, operations):
        super(JsonWriteTask, self).__init__(executor, operations)

        self.decoder = None

    @property
    def state(self):
        state = super(JsonWriteTask, self).state

        if self.decoder is None or state == Task.State.created:
            return Task.State.created

        if self.decoder.closed or state == Task.State.closed:
            return Task.State.closed

        return Task.State.started

    def decode(self):
        return self.decoder.items()

    def encode(self, revision, items):
        # Create encoder
        encoder = JsonEncoder(
            revision.stream,
            indent=4
        )

        # Encode items, and write to revision stream
        encoder.write_dict(items)

    def open(self):
        super(JsonWriteTask, self).open()

        # Create decoder
        self.decoder = JsonDecoder(self.stream)

    def close(self):
        if not super(JsonWriteTask, self).close():
            return False

        # Close decoder
        if self.decoder:
            self.decoder.close()

        return True
