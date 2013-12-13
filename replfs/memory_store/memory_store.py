from time import time
from stat import S_IFDIR, S_IFLNK, S_IFREG
import logging
import pprint
class MemoryStore:

    def __init__(self, config_hash):
        self.config = config_hash
        self.debug("Initializing MemoryStore")
        self.paths = {}
        self.new_dir("/")

    def add_dir(self, path, mode):
        self.debug('add_dir', path, mode)
        self.new_dir(path)
        parent_path = "/" + "/".join(path.split("/")[1:-1])
        dirname = path.split('/')[-1]
        if parent_path in self.paths:
            self.add_dir_entry(parent_path, dirname, path)

    def new_dir(self, path, mode=0):
        self.debug('new_dir', path)
        if path not in self.paths:
            self.paths[path] = {
                'entries': {},
                'type': 'dir',
                'st_mode': (S_IFDIR | mode),
                'st_nlink': 2,
                'st_size': 0,
                'st_ctime': time(),
                'st_mtime': time(),
                'st_atime': time()
            }

    def rmdir(self, path):
        if self.exists(path):
            del self.paths[path]
            return True
        else:
            return False

    def add_dir_entry(self, dir_path, name, path):
        dir_path = "/" + dir_path.strip("/")
        path = "/" + path.strip("/")
        self.debug('add_dir_entry', dir_path, name, path)
        self.paths[dir_path]['entries'][name] = path

    def is_dir(self, path):
        return self.paths[path]['type'] == 'dir'

    def get_dir_entries(self, path):
        return self.paths[path]['entries']

    def get_dir(self, path):
        if self.paths[path]['type'] == 'dir':
            return self.paths[path]
        else:
            return None

    def get_bricks_for_path(self, path):
        if self.paths[path]['type'] == 'file':
            return self.paths[path]['bricks']
        else:
            return False

    def exists(self, path):
        return path in self.paths

    def set_bricks_for_path(self, path, bricks):
        if path in self.paths:
            if self.paths[path]['type'] == 'file':
                self.paths[path]['bricks'] = bricks
            else:
                print("error")
        else:
            self.paths[path] = {
                "type": "file",
                "bricks": bricks
            }

    def debug(self, *args):
        if self.config['debug_memory_store']:
            nargs = ("MSTORE", args)
            logging.debug(nargs)

