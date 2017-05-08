from __future__ import absolute_import, division, print_function

from byte.executors.file.lock.base import BaseFileLock, FileLockError

import msvcrt
import os
import six

if six.PY2:
    def is_file(fp):
        return type(fp) is file
else:
    import io

    def is_file(fp):
        return isinstance(fp, io.IOBase)


class BaseMsvcrtFileLock(BaseFileLock):
    def release(self):
        try:
            # Save current position, and seek to the start
            if is_file(self.fp):
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
            if is_file(self.fp):
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
            if is_file(self.fp):
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
