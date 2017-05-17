from threading import RLock

try:
    from thread import get_ident
except ImportError:
    from threading import get_ident


class LocalManager(object):
    def __init__(self):
        self._bindings = {}
        self._lock = RLock()

    def create(self):
        raise NotImplementedError

    def detach(self, item):
        with self._lock:
            if not item._ident:
                return

            # Remove item from collection
            self._bindings.pop(item._ident)

            # Remove ident from item
            item._ident = None

            # Fire `on_detached` callback
            self.on_detached(item)

    def get(self, state=False, **kwargs):
        ident = get_ident()

        try:
            created = False
            item = self._bindings[ident]
        except KeyError:
            created, item = self._acquire(ident, **kwargs)

        if state:
            return created, item

        return item

    def acquire(self, **kwargs):
        return True, self.create()

    def on_created(self, item):
        pass

    def on_detached(self, item):
        pass

    def _acquire(self, ident=None, **kwargs):
        if not ident:
            ident = get_ident()

        with self._lock:
            # Return existing item (if available)
            if ident in self._bindings:
                return False, self._bindings[ident]

            # Acquire item
            created, item = self.acquire(**kwargs)

            if not item:
                return False, None

            if created:
                if not isinstance(item, LocalItem):
                    raise ValueError('Invalid item (expected instance of LocalItem)')

                # Set item manager
                item._manager = self

                # Fire `on_created` callback
                self.on_created(item)

            # Bind item to ident
            return created, self._bind(item, ident)

    def _bind(self, item, ident):
        # Set item ident
        item._ident = ident

        # Store item in bindings
        self._bindings[ident] = item

        return item

    def __len__(self):
        return len(self._bindings)


class LocalItem(object):
    def __init__(self):
        self._ident = None
        self._manager = None

    def detach(self):
        if not self._manager or not self._ident:
            return

        self._manager.detach(self)
