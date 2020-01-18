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

    #if self.auth.verificationCode != True:
    #    self.fuse_exit()

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
        #self.auth.log(message="Action: ACCESS | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)
            
    def chmod(self, path, mode):
        self.auth.log(message="Action: CHMOD | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)
            
    def chown(self, path, uid, gid):
        self.auth.log(message="Action: CHOWN | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)
            
    def getattr(self, path, fh=None):
        #self.auth.log(message="Action: GEATATTR | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
            
    def readdir(self, path, fh):
        #self.auth.log(message="Action: READDIR | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r
            
    def readlink(self, path):
        self.auth.log(message="Action: READLINK | Path:" + self._full_path(path))
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname
            
    def mknod(self, path, mode, dev):
        self.auth.log(message="Action: MKNOD | Path:" + self._full_path(path))
        return os.mknod(self._full_path(path), mode, dev)
            
    def rmdir(self, path):
        self.auth.log(message="Action: RMDIR | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        return os.rmdir(full_path)
            
    def mkdir(self, path, mode):
        self.auth.log(message="Action: MKDIR | Path:" + self._full_path(path))
        return os.mkdir(self._full_path(path), mode)
            
    def statfs(self, path):
        #self.auth.log(message="Action: STATFS | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))
            
    def unlink(self, path):
        self.auth.log(message="Action: UNLINK | Path:" + self._full_path(path))
        return os.unlink(self._full_path(path))
            
    def symlink(self, name, target):
        self.auth.log(message="Action: SYMLINK | Path:" + self._full_path(path))
        return os.symlink(target, self._full_path(name))
            
    def rename(self, old, new):
        self.auth.log(message="Action: RENAME | Path:" + self._full_path(path))
        return os.rename(self._full_path(old), self._full_path(new))
            
    def link(self, target, name):
        self.auth.log(message="Action: LINK | Path:" + self._full_path(path))
        return os.link(self._full_path(name), self._full_path(target))
            
    def utimens(self, path, times=None):
        self.auth.log(message="Action: ULTIMENS | Path:" + self._full_path(path))
        return os.utime(self._full_path(path), times)
            
    # File methods
    # ============

    def open(self, path, flags):
        #verification = self.auth.verification()
        if self.auth.verification == True:
            self.auth.log(message="Action: OPEN | Path:" + self._full_path(path))
            full_path = self._full_path(path)
            return os.open(full_path, flags)
        else:
            self.auth.log(message="Action: OPEN ERROR - VALIDATE FIRST!! | Path:" + self._full_path(path))
            print("Erro: primeiro validade na APP para usar o comando OPEN")
            return 0
            
    def create(self, path, mode, fi=None):
        self.auth.log(message="Action: CREATE | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
            
    def read(self, path, length, offset, fh):
        self.auth.log(message="Action: READ | Path:" + self._full_path(path))
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        self.auth.log(message="Action: WRITE | Path:" + self._full_path(path))
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)
            
    def truncate(self, path, length, fh=None):
        self.auth.log(message="Action: TRUNCATE | Path:" + self._full_path(path))
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)
            
    def flush(self, path, fh):
        self.auth.log(message="Action: FLUSH | Path:" + self._full_path(path))
        return os.fsync(fh)
            
    def release(self, path, fh):
        self.auth.log(message="Action: RELEASE | Path:" + self._full_path(path))
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        self.auth.log(message="Action: FSYNC | Path:" + self._full_path(path))
        return self.flush(path, fh)


    #Ignorar, teste
    def stop(self):
        fuse.fuse_exit()

def main(root=None, mountpoint=None, auth=None):
    auth = auth
    if root==None or mountpoint==None:
        dirname = os.path.dirname(__file__)
        mountpoint = os.path.join(dirname, 'mountpoint')
        root = os.path.join(dirname, 'storage')
    #if auth.user:
    #   auth.log(message="Action: Start Libfuse - Login ok")
    FUSE(Passthrough(root, auth), mountpoint, nothreads=True, foreground=True)
    #else:
    #    auth.log(message="Action: Start Libfuse failed - Not Loged in")

if __name__ == '__main__':
    from core import authentication
    auth = authentication.Auth(username=sys.argv[3], password=sys.argv[4])
    if auth.user:
        auth.log(message="Action: Start Libfuse - Login ok")
        main(root=sys.argv[2], mountpoint=sys.argv[1], auth=auth)
    else:
        auth.log(message="Action: Start Libfuse failed - Not loged in")