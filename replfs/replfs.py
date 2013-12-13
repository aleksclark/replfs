#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import hashlib
import pprint
import logging

from fuse import FUSE, FuseOSError, Operations
from errno import ENOENT
from random import sample, choice

from replfs.memory_store.memory_store import MemoryStore

class ReplFS(Operations):
    def __init__(self, config):
        self.config = config
        logging.basicConfig(filename=config['log_file'],level=logging.DEBUG)
        self.root = self.config['bricks'][0]
        self.bricks = config['bricks']
        if self.config['metadata_store'] == 'memory':
            print('using memory_store')
            self.store = MemoryStore(config)


    # Helpers
    # =======
    # WORKING ON DIS
    def _full_path(self, partial):
        
        self.debug('full path called for', partial)
        brick_root = None
        # if partial.startswith("/"):
        #     partial = partial[1:]
        if self.store.exists(partial):
            brick_root = choice(self.store.get_bricks_for_path(partial))
            path_hash = hashlib.sha1(partial.encode()).hexdigest()
            path = brick_root + "/" + path_hash
            return path
        else:
            return False
        # else:
        #     # print("adding")
        #     #this should be a new file, NOT a new dir...
        #     file_name = partial.split("/")[-1]
        #     dest_dir = partial.replace(file_name, "")
        #     # print(dest_dir)
        #     # print(file_name)
        #     self.store.add_dir_entry(dest_dir, file_name, partial)
        #     dest_bricks = sample(self.bricks, self.config['replication_level'])
        #     self.store.set_bricks_for_path(partial, dest_bricks)
        #     brick_root = choice(dest_bricks)

        

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        self.debug('access', path, mode)
        # full_path = self._full_path(path)
        # if not os.access(full_path, mode):
        #     raise FuseOSError(errno.EACCES)
        pass

    def chmod(self, path, mode):
        self.debug('chmod', path, mode)
        # full_path = self._full_path(path)
        # return os.chmod(full_path, mode)
        pass

    def chown(self, path, uid, gid):
        self.debug('chown', path, mode)
        # full_path = self._full_path(path)
        # return os.chown(full_path, uid, gid)
        pass

    def getattr(self, path, fh=None):
        self.debug('getattr', path, fh)
        if self.store.exists(path):
            if not self.store.is_dir(path):
                full_path = self._full_path(path)
                st = os.lstat(full_path)
                return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                    'st_mode', 'st_mtime', 'st_nlink', 'st_size'))
            else:
                return self.store.get_dir(path)
        else:
            raise FuseOSError(ENOENT)


    def readdir(self, path, fh):
        self.debug('readdir', path, fh)
        dirents = ['.', '..']
        if self.store.is_dir(path):
            dirents.extend(self.store.get_dir_entries(path))
        for r in dirents:
            yield r

    def readlink(self, path):
        print("readlink" + path)
        self.debug("readlink", path)
        # pathname = os.readlink(self._full_path(path))
        # if pathname.startswith("/"):
        #     # Path name is absolute, sanitize it.
        #     return os.path.relpath(pathname, self.root)
        # else:
        #     return pathname
        pass

    def mknod(self, path, mode, dev):
        logger.debug("mknod - " + path + " ")
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        return self.store.rmdir(path)

    def mkdir(self, path, mode):
        return self.store.add_dir(path, mode)
        # return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        pass

    def symlink(self, target, name):
        pass

    def rename(self, old, new):
        pass

    def link(self, target, name):
        pass

    def utimens(self, path, times=None):
        pass

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print("create" + path)
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print("write" + path)
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

    def debug(self, *args):
        if self.config['debug_repl']:
            nargs = ("REPL", args)
            logging.debug(nargs)