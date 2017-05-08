from __future__ import absolute_import, division, print_function

from byte.executors.file.lock.base import BaseFileLock, FileLockError

import win32con
import win32file
import pywintypes


class BaseWin32FileLock(BaseFileLock):
    def __init__(self, fp):
        super(BaseWin32FileLock, self).__init__(fp)

        # Retrieve win32 file handle
        self.handle = win32file._get_osfhandle(self.fp.fileno())

    def release(self):
        # Unlock file
        try:
            win32file.UnlockFileEx(self.handle, 0, 0x7fff0000, pywintypes.OVERLAPPED())
        except Exception as ex:
            raise FileLockError(ex)


class Win32ExclusiveFileLock(BaseWin32FileLock):
    def acquire(self, blocking=None):
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = win32con.LOCKFILE_EXCLUSIVE_LOCK

        if not blocking:
            mode += win32con.LOCKFILE_FAIL_IMMEDIATELY

        # Lock file
        try:
            win32file.LockFileEx(self.handle, mode, 0, 0x7fff0000, pywintypes.OVERLAPPED())
        except Exception as ex:
            raise FileLockError(ex)


class Win32SharedFileLock(BaseWin32FileLock):
    def acquire(self, blocking=None):
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = 0

        if not blocking:
            mode += win32con.LOCKFILE_FAIL_IMMEDIATELY

        # Lock file
        try:
            win32file.LockFileEx(self.handle, mode, 0, 0x7fff0000, pywintypes.OVERLAPPED())
        except Exception as ex:
            raise FileLockError(ex)

