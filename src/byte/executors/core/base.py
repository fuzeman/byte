from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types


class Executor(object):
    def __init__(self, collection, model):
        self.collection = collection
        self.model = model

        self._compiler = None

    @property
    def compiler(self):
        if not self._compiler:
            self._compiler = self.construct_compiler()

        return self._compiler

    @property
    def plugins(self):
        if not self.collection:
            return None

        return self.collection.plugins

    def close(self):
        raise NotImplementedError

    def execute(self, statement):
        raise NotImplementedError

    def construct_compiler(self):
        return self.plugins.get_compiler('simple')(self)


class ExecutorPlugin(Executor, Plugin):
    key = None
    priority = Plugin.Priority.Medium

    class Meta(Plugin.Meta):
        kind = 'executor'

        content_type = None
        extension = None
        scheme = None

        @classmethod
        def transform(cls):
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Medium, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Medium, value)
            )

            cls.scheme = resolve_tuples(
                cls.scheme,
                lambda value: (Plugin.Priority.Medium, value)
            )

        @classmethod
        def validate(cls, compiler):
            assert compiler.key, (
                'Plugin has no "key" attribute defined'
            )

            assert isinstance(compiler.key, string_types), (
                'Invalid value provided for the plugin "key" attribute (expected str)'
            )

            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )

            assert is_list_of(cls.scheme, (int, string_types)), (
                'Invalid value provided for the "scheme" attribute (expected str, [str], [(int, str)])'
            )

            assert len(cls.scheme) > 0, (
                'Invalid value provided for the "scheme" attribute (at least one scheme is required)'
            )


class SimpleExecutor(Executor):
    def insert(self, items):
        raise NotImplementedError

    def items(self):
        raise NotImplementedError


class SimpleExecutorPlugin(SimpleExecutor, ExecutorPlugin):
    pass


class FormatExecutor(SimpleExecutor):
    def __init__(self, collection, model):
        super(FormatExecutor, self).__init__(collection, model)

        self._format = None

    @property
    def format(self):
        if not self._format:
            self._format = self.construct_format()

        return self._format

    def construct_format(self):
        raise NotImplementedError


class FormatExecutorPlugin(FormatExecutor, ExecutorPlugin):
    pass
