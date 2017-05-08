from byte.executors.core.models import Revision
from byte.executors.file.lock import ExclusiveFileLock

from tempfile import NamedTemporaryFile
import os
import shutil


class FileRevision(Revision):
    def __init__(self, executor):
        super(FileRevision, self).__init__(executor)

        self.revert_path = os.path.join(
            self.executor.directory,
            '%s.revert%s' % (self.executor.name, self.executor.extension)
        )

        # Open temporary revision file
        self.stream = NamedTemporaryFile(
            prefix=self.executor.name + '.',
            suffix=self.executor.extension,
            dir=self.executor.directory,
            delete=False
        )

    def replace(self, fp):
        try:
            # Seek revision file to start
            self.stream.seek(0)

            # Copy revision to collection file
            shutil.copyfileobj(self.stream, fp)
        except Exception as ex:
            # Error raised, revert revision
            self.revert(fp)
            raise ex
        finally:
            # Delete revert file
            os.remove(self.revert_path)

    def revert(self, fp):
        # Revert collection to backup contents
        with open(self.revert_path, 'r') as rp:
            shutil.copyfileobj(rp, fp)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Create copy of current collection (for reverting on errors)
        shutil.copy2(self.executor.path, self.revert_path)

        # Replace collection file with revision (inside exclusive lock)
        try:
            with open(self.executor.path, 'w') as fp:
                with ExclusiveFileLock(fp):
                    self.replace(fp)
        finally:
            # Close revision file
            self.stream.close()

            # Delete revision file
            os.remove(self.stream.name)
