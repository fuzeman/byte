class BaseFileLock(object):
    def __init__(self, fp, blocking=True):
        self.fp = fp

        self.blocking = blocking

    def acquire(self, blocking=None):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class FileLockError(Exception):
    pass
