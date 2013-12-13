#!/usr/bin/env python
import yaml
from fuse import FUSE
from replfs.replfs import ReplFS

def main(mountpoint, config):
    conf_stream = open(config, 'r')
    config_hash = yaml.load(conf_stream)
    print(config_hash)
    FUSE(ReplFS(config_hash), mountpoint, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])