"""byte - base engine module."""
from __future__ import absolute_import, division, print_function

from byte.core.plugin.manager import PluginManager


class Engine(object):
    """Base engine class."""

    def __init__(self, plugins=None):
        """Create engine.

        :param plugins: Plugins to enable (or :code:`None` to enable all plugins)
        :type plugins: list of module
        """
        self.plugins = PluginManager(plugins)
