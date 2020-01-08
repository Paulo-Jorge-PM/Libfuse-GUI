#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from views import gui
from core import authentication, tools

class Main:

    def __init__(self):
        self.configs = self.readConfigs()
        #self.checkDirs(self.configs[1], self.configs[2])

        tools.checkDirs(self.configs[1], self.configs[2])

        self.auth = authentication.Auth(self.configs)
        self.gui = self.setGui()

    def readConfigs(self):
        #to do: read constants from the config file instead
        GUI = "webview"
        dirname = os.path.dirname(__file__)
        MOUNTPOINT = os.path.join(dirname, 'models/mountpoint')
        print(MOUNTPOINT)
        #MOUNTPOINT = "/dev/libfuse"
        ROOTPATH = os.path.join(dirname, 'models/storage')
        return(GUI, MOUNTPOINT, ROOTPATH)

    def setGui(self):
        if self.configs[0] == "webview": 
            return gui.Gui(configs=self.configs, auth=self.auth)

    def checkDirs(self, mountpoint, root):
        try:
            if not os.path.exists(mountpoint):
                os.makedirs(mountpoint)
            if not os.path.exists(root):
                os.makedirs(root)
        except:
            pass

if __name__ == '__main__':
    main = Main()
