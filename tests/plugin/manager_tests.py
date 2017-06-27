from __future__ import absolute_import, division, print_function

from byte.core.plugin.manager import PluginManager
import byte.executors.memory


def test_discovery():
    """Test plugins can be discovered."""
    plugins = PluginManager()

    # Ensure the core executors have been registered
    assert 'byte.executors.file:database' in plugins
    assert 'byte.executors.file:table' in plugins

    assert 'byte.executors.memory:database' in plugins
    assert 'byte.executors.memory:table' in plugins


def test_provided_modules():
    """Test plugins can be resolved from modules."""
    plugins = PluginManager([
        byte.executors.memory
    ])

    # Ensure only one plugin exists
    assert len(plugins) == 2

    # Ensure memory executor has been registered
    assert 'byte.executors.memory:database' in plugins
    assert 'byte.executors.memory:table' in plugins
