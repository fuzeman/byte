from byte.executors.core.models import Revision

from copy import deepcopy


class MemoryRevision(Revision):
    def __init__(self, executor):
        super(MemoryRevision, self).__init__(executor)

        self.revert_items = {}
        self.items = {}

    def replace(self):
        try:
            # Replace collection items
            self.executor.items = self.items
        except Exception as ex:
            # Error raised, revert revision
            self.revert()
            raise ex
        finally:
            # Delete revert items
            self.revert_items = None

    def revert(self):
        # Revert collection to backup items
        self.executor.items = self.revert_items

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Create copy of current collection (for reverting on errors)
        self.revert_items = deepcopy(self.executor.items)

        # Replace collection file with revision
        try:
            self.replace()
        finally:
            # Delete revision items
            self.items = None
