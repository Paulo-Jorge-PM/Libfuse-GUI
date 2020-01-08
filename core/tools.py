#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

def checkDirs(mountpoint, root):
    try:
        if not os.path.exists(mountpoint):
            os.makedirs(mountpoint)
        if not os.path.exists(root):
            os.makedirs(root)
    except:
        pass
