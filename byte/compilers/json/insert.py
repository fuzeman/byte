from byte.compilers.core.base import Compiler


class JsonInsertCompiler(Compiler):
    def compile(self, statement):
        raise NotImplementedError
