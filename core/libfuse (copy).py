#!/usr/bin/env python

"""
Adapted from: https://github.com/skorokithakis/python-fuse-sample
"""

from __future__ import with_statement

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations, fuse_exit


class Passthrough(Operations):
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)
        """verification = self.auth.verification(message="Action: ACCESS | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            if not os.access(full_path, mode):
                raise FuseOSError(errno.EACCES)
        else:
            return 0"""
            
    def chmod(self, path, mode):
        verification = self.auth.verification(message="Action: CHMOD | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            return os.chmod(full_path, mode)
        else:
            return 0
            
    def chown(self, path, uid, gid):
        verification = self.auth.verification(message="Action: CHOWN | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            return os.chown(full_path, uid, gid)
        else:
            return 0
            
    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        """verification = self.auth.verification(message="Action: GETATTR | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            st = os.lstat(full_path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                         'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        else:
            return 0"""
            
    def readdir(self, path, fh):
        verification = self.auth.verification(message="Action: READDIR | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            dirents = ['.', '..']
            if os.path.isdir(full_path):
                dirents.extend(os.listdir(full_path))
            for r in dirents:
                yield r
        else:
            return []
            
    def readlink(self, path):
        verification = self.auth.verification(message="Action: READLINK | Path:" + self._full_path(path))
        if verification == True:
            pathname = os.readlink(self._full_path(path))
            if pathname.startswith("/"):
                # Path name is absolute, sanitize it.
                return os.path.relpath(pathname, self.root)
            else:
                return pathname
        else:
            return 0
            
    def mknod(self, path, mode, dev):
        verification = self.auth.verification(message="Action: MKNOD | Path:" + self._full_path(path))
        if verification == True:
            return os.mknod(self._full_path(path), mode, dev)
        else:
            return 0
            
    def rmdir(self, path):
        verification = self.auth.verification(message="Action: RMDIR | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            return os.rmdir(full_path)
        else:
            return 0
            
    def mkdir(self, path, mode):
        verification = self.auth.verification(message="Action: MKDIR | Path:" + self._full_path(path))
        if verification == True:
            return os.mkdir(self._full_path(path), mode)
        else:
            return 0
            
    def statfs(self, path):
        verification = self.auth.verification(message="Action: STATFS | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            stv = os.statvfs(full_path)
            return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
                'f_frsize', 'f_namemax'))
        else:
            return 0
            
    def unlink(self, path):
        verification = self.auth.verification(message="Action: UNLINK | Path:" + self._full_path(path))
        if verification == True:
            return os.unlink(self._full_path(path))
        else:
            return 0
            
    def symlink(self, name, target):
        verification = self.auth.verification(message="Action: SYMLINK | Path:" + self._full_path(path))
        if verification == True:
            return os.symlink(target, self._full_path(name))
        else:
            return 0
            
    def rename(self, old, new):
        verification = self.auth.verification(message="Action: RENAME | Path:" + self._full_path(path))
        if verification == True:
            return os.rename(self._full_path(old), self._full_path(new))
        else:
            return 0
            
    def link(self, target, name):
        verification = self.auth.verification(message="Action: LINK | Path:" + self._full_path(path))
        if verification == True:
            return os.link(self._full_path(name), self._full_path(target))
        else:
            return 0
            
    def utimens(self, path, times=None):
        verification = self.auth.verification(message="Action: ULTIMENS | Path:" + self._full_path(path))
        if verification == True:
            return os.utime(self._full_path(path), times)
        else:
            return 0
            
    # File methods
    # ============

    def open(self, path, flags):
        verification = self.auth.verification(message="Action: OPEN | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            return os.open(full_path, flags)
        else:
            return 0

    def create(self, path, mode, fi=None):
        verification = self.auth.verification(message="Action: CREATE | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        else:
            return 0
            
    def read(self, path, length, offset, fh):
        verification = self.auth.verification(message="Action: READ | Path:" + self._full_path(path))
        if verification == True:
            os.lseek(fh, offset, os.SEEK_SET)
            return os.read(fh, length)
        else:
            return 0

    def write(self, path, buf, offset, fh):
        verification = self.auth.verification(message="Action: WRITE | Path:" + self._full_path(path))
        if verification == True:
            os.lseek(fh, offset, os.SEEK_SET)
            return os.write(fh, buf)
        else:
            return 0
            
    def truncate(self, path, length, fh=None):
        verification = self.auth.verification(message="Action: TRUNCATE | Path:" + self._full_path(path))
        if verification == True:
            full_path = self._full_path(path)
            with open(full_path, 'r+') as f:
                f.truncate(length)
        else:
            return 0
            
    def flush(self, path, fh):
        verification = self.auth.verification(message="Action: FLUSH | Path:" + self._full_path(path))
        if verification == True:
            return os.fsync(fh)
        else:
            return 0
            
    def release(self, path, fh):
        verification = self.auth.verification(message="Action: RELEASE | Path:" + self._full_path(path))
        if verification == True:
            return os.close(fh)
        else:
            return 0

    def fsync(self, path, fdatasync, fh):
        verification = self.auth.verification(message="Action: FSYNC | Path:" + self._full_path(path))
        if verification == True:
            return self.flush(path, fh)
        else:
            return 0


    #Ignorar, teste
    def stop(self):
        fuse.fuse_exit()

def main(root=None, mountpoint=None, auth=None):
    auth = auth
    if root==None or mountpoint==None:
        dirname = os.path.dirname(__file__)
        mountpoint = os.path.join(dirname, 'mountpoint')
        root = os.path.join(dirname, 'storage')
    FUSE(Passthrough(root, auth), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    from core import authentication
    main(root=sys.argv[2], mountpoint=sys.argv[1], auth=authentication.Auth(username=sys.argv[3], password=sys.argv[4]))