"""byte - base engine module."""
from __future__ import absolute_import, division, print_function

from byte.core.plugin.manager import PluginManager


class Engine(object):
    """Base engine class."""

    def __init__(self, plugins=None):
        self.plugins = PluginManager(plugins)
