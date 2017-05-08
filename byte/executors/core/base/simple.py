"""Simple executor base module."""

from __future__ import absolute_import, division, print_function

from byte.executors.core.base.executor import Executor, ExecutorPlugin


class SimpleExecutor(Executor):
    def revision(self):
        raise NotImplementedError


class SimpleExecutorPlugin(SimpleExecutor, ExecutorPlugin):
    pass
