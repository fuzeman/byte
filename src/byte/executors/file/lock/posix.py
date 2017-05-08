from byte.executors.file.lock.base import BaseFileLock, FileLockError

import fcntl


class BasePosixFileLock(BaseFileLock):
    def release(self):
        # Unlock file
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_UN)
        except Exception as ex:
            raise FileLockError(ex)


class PosixExclusiveFileLock(BasePosixFileLock):
    def acquire(self, blocking=None):
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = fcntl.LOCK_EX

        if not blocking:
            mode |= fcntl.LOCK_NB

        # Lock file
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_EX)
        except Exception as ex:
            raise FileLockError(ex)


class PosixSharedFileLock(BasePosixFileLock):
    def acquire(self, blocking=None):
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = fcntl.LOCK_SH

        if not blocking:
            mode |= fcntl.LOCK_NB

        # Lock file
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_SH)
        except Exception as ex:
            raise FileLockError(ex)

