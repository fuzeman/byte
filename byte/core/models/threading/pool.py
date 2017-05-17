from byte.core.models.threading.local import LocalItem, LocalManager

try:
    from thread import get_ident
except ImportError:
    from threading import get_ident


class PoolManager(LocalManager):
    def __init__(self, maximum=None):
        super(PoolManager, self).__init__()

        self.maximum = maximum

        self._all = []
        self._available = []

    @property
    def active(self):
        return len(self._all) - len(self._available)

    def acquire(self, blocking=False):
        # Use available item (if one exists)
        if self._available:
            return False, self._available.pop()

        # Create item (if below maximum)
        if self.maximum is None or len(self._all) < self.maximum:
            return True, self.create()

        # Blocking disabled, just return `None`
        if not blocking:
            return False, None

        # Wait for available item
        raise NotImplementedError

    def on_created(self, item):
        self._all.append(item)

    def on_detached(self, item):
        self._available.append(item)

    def __len__(self):
        return len(self._all)


class PoolItem(LocalItem):
    pass
