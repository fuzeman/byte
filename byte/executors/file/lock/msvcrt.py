from byte.executors.file.lock.base import BaseFileLock, FileLockError

import msvcrt
import os


class BaseMsvcrtFileLock(BaseFileLock):
    def release(self):
        try:
            # Save current position, and seek to the start
            if type(self.fp) == file:
                fn = self.fp.fileno()
                pos = self.fp.tell()

                self.fp.seek(0)
            else:
                fn = self.fp
                pos = os.lseek(fn, 0, 0)

                os.lseek(fn, 0, 0)

            # Unlock file
            try:
                msvcrt.locking(fn, msvcrt.LK_UNLCK, -1)
            finally:
                # Seek back to original position
                os.lseek(fn, pos, 0)
        except Exception as ex:
            raise FileLockError(ex)


class MsvcrtExclusiveFileLock(BaseMsvcrtFileLock):
    def acquire(self, blocking=None):
        if blocking is None:
            blocking = self.blocking

        try:
            # Save current position, and seek to the start
            if type(self.fp) == file:
                fn = self.fp.fileno()
                pos = self.fp.tell()

                self.fp.seek(0)
            else:
                fn = self.fp
                pos = os.lseek(fn, 0, 0)

                os.lseek(fn, 0, 0)

            # Unlock file
            try:
                msvcrt.locking(fn, msvcrt.LK_LOCK if blocking else msvcrt.NBLCK, -1)
            finally:
                # Seek back to original position
                os.lseek(fn, pos, 0)
        except Exception as ex:
            raise FileLockError(ex)


class MsvcrtSharedFileLock(BaseMsvcrtFileLock):
    def acquire(self, blocking=None):
        if blocking is None:
            blocking = self.blocking

        try:
            # Save current position, and seek to the start
            if type(self.fp) == file:
                fn = self.fp.fileno()
                pos = self.fp.tell()

                self.fp.seek(0)
            else:
                fn = self.fp
                pos = os.lseek(fn, 0, 0)

                os.lseek(fn, 0, 0)

            # Unlock file
            try:
                msvcrt.locking(fn, msvcrt.LK_RLCK if blocking else msvcrt.NBRLCK, -1)
            finally:
                # Seek back to original position
                os.lseek(fn, pos, 0)
        except Exception as ex:
            raise FileLockError(ex)