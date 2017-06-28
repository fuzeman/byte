"""byte - plugin manager module."""

from __future__ import absolute_import, division, print_function

from byte import __path__ as byte_path
from byte.core.plugin.base import Plugin

import imp
import inspect
import logging
import os
import pkgutil
import six
import sys

log = logging.getLogger(__name__)


class PluginManager(object):
    """Plugin manager class."""

    kinds = [
        Plugin.Kind.Compiler,
        Plugin.Kind.Executor,
        Plugin.Kind.Format
    ]

    def __init__(self, modules=None):
        """Create plugin manager.

        :param modules: Default plugin modules
        :type modules: list of module or None
        """
        # Plugins
        self.plugins = {}
        self.plugins_by_kind = {}

        # Update plugin registry
        self.update(modules, reset=False)

    @classmethod
    def discover(cls, packages=('compilers', 'executors', 'formats')):
        """Discover plugin modules.

        :param packages: Package names
        :type packages: tuple of str
        """
        scanned_paths = set()

        for search_path in byte_path:
            search_path = os.path.normcase(os.path.normpath(
                os.path.realpath(search_path)
            ))

            if search_path in scanned_paths:
                continue

            scanned_paths.add(search_path)

            # Scan `search_path` for `packages`
            for package in packages:
                # Find package
                try:
                    _, package_path, _ = imp.find_module(package, [search_path])
                except ImportError:
                    continue

                # Discover plugins in package
                for mod in cls.discover_package(package, package_path):
                    yield mod

    @staticmethod
    def discover_package(package, package_path):
        """Discover plugin modules in package.

        :param package: Package name
        :type package: str

        :param package_path: Package path
        :type package_path: str
        """
        # Iterate over modules in package
        for _, name, _ in pkgutil.iter_modules([package_path]):
            # Find module
            try:
                fp, module_path, description = imp.find_module(name, [package_path])
            except ImportError as ex:
                log.warn('Unable to find module \'%s\' in %r: %s', name, package_path, ex)
                continue

            # Return existing module (if available)
            full_name = 'byte.%s.%s' % (package, name)

            if full_name in sys.modules:
                yield sys.modules[full_name]
                continue

            # Import module
            try:
                yield imp.load_module(full_name, fp, module_path, description)
            except ImportError as ex:
                log.warn('Unable to load module \'%s\' in %r: %s', name, module_path, ex)
                continue

    def get(self, id):
        """Retrieve plugin by identifier.

        Note: Raises a :code:`ValueError` exception if the plugin doesn't exist.

        :raises: ValueError
        :return: Plugin
        :rtype: byte.core.plugin.base.Plugin
        """
        plugin = self.plugins.get(id)

        if not plugin:
            raise ValueError('No plugin found with id: %s' % (id,))

        return plugin

    #
    # Match
    #

    def match(self, kind, **filters):
        """Get plugin.

        Raises :code:`ValueError` on unknown plugin type or key.

        :param kind: Plugin type
        :type kind: str

        :param key: Plugin key
        :type key: str
        """
        if kind not in self.kinds:
            raise ValueError('Unknown plugin kind: %s' % (kind,))

        # Retrieve plugins matching `kind`
        plugins = self.plugins_by_kind.get(kind)

        if not plugins:
            raise ValueError('No \'%s\' plugins have been registered' % (kind,))

        # Find matching plugins
        matches = []

        for plugin in six.itervalues(plugins):
            meta = getattr(plugin, 'Meta')

            if not meta:
                continue

            # Ensure ordered properties match, and build the order key
            valid, pending, order = self._match_ordered(meta, filters)

            if not valid:
                continue

            # Ensure basic properties match
            if not self._match_basic(meta, pending):
                continue

            # Add plugin to list
            matches.append((tuple(order), plugin))

        # Ensure plugins were found
        if not matches:
            raise ValueError('No \'%s\' plugin found matching filters' % (kind,))

        # Sort matched plugins (by order)
        matches.sort()

        return matches[0][1]

    @staticmethod
    def _match_ordered(meta, filters):
        pending = filters.copy()
        order = []

        for key in meta.order_by:
            if key not in pending:
                continue

            expected = pending.pop(key)
            matched = False

            for priority, value in getattr(meta, key):
                if value == expected:
                    order.append(priority)
                    matched = True
                    break

            if not matched:
                return False, pending, order

        return True, pending, order

    @staticmethod
    def _match_basic(meta, filters):
        for key, expected in six.iteritems(filters):
            if not hasattr(meta, key):
                return False

            value = getattr(meta, key)

            # Handle "any" engine definition
            if key == 'engine' and value == Plugin.Engine.Any:
                continue

            # Check value matches
            if value != expected:
                return False

        return True

    #
    # Register
    #

    def register(self, plugin):
        """Register plugin.

        :param plugin: Plugin
        """
        plugin.id = plugin.__module__.replace('.main', '')

        if plugin.key:
            plugin.id += ':%s' % (plugin.key,)

        # Resolve plugin meta
        meta = getattr(plugin, 'Meta', None)

        if not meta:
            log.warn('Plugin \'%s\' has no meta defined', plugin.id)
            return False

        # Transform plugin meta values
        meta.transform(plugin)

        # Validate plugin meta
        try:
            meta.validate(plugin)
        except AssertionError as ex:
            log.warn('Plugin \'%s\' failed validation: %s', plugin.id, ex.message)
            return False

        # Ensure plugin `meta.kind` collection exists
        if meta.kind not in self.plugins_by_kind:
            self.plugins_by_kind[meta.kind] = {}

        # Ensure plugin hasn't already been registered
        if plugin.id in self.plugins or plugin.id in self.plugins_by_kind[meta.kind]:
            log.warn('Plugin with kind \'%s\' and key \'%s\' has already been registered', meta.kind, plugin.id)
            return False

        # Register plugin
        self.plugins[plugin.id] = plugin
        self.plugins_by_kind[meta.kind][plugin.id] = plugin

        log.debug('Registered %s \'%s\'', meta.kind, plugin.id)
        return True

    def reset(self):
        """Reset plugin registry."""
        self.plugins = {}
        self.plugins_by_kind = {}

    def update(self, modules=None, reset=True):
        """Update plugins registry.

        :param modules: Modules to scan for plugins
        :type modules: list of module

        :param reset: Reset registry
        :type reset: bool
        """
        # Reset state (if enabled)
        if reset:
            self.reset()

        # Find (and register) plugin classes in `modules`
        for mod in (modules or self.discover()):
            for key, value in mod.__dict__.items():
                if key.startswith('_') or not inspect.isclass(value):
                    continue

                if value.__module__ != mod.__name__ and value.__module__ != mod.__name__ + '.main':
                    continue

                if not issubclass(value, Plugin):
                    continue

                self.register(value)

    @staticmethod
    def _resolve_definition(value):
        if type(value) is tuple and len(value) == 2:
            return value

        return 1000, value

    def __contains__(self, key):
        return key in self.plugins

    def __len__(self):
        return len(self.plugins)
