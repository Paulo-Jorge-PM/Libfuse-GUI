#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from views import gui
from core import authentication, tools

class Main:

    def __init__(self):
        self.configs = self.readConfigs()

        #remove old mount folder 1st, sometimes give error if not empty
        try:
            tools.removeMount(self.configs[1])
        except:
            pass

        tools.createDir(self.configs[1])
        tools.createDir(self.configs[2])

        self.auth = authentication.Auth(configs=self.configs)
        self.gui = self.setGui()

    def readConfigs(self):
        #to do: read constants from a config file instead
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

if __name__ == '__main__':
    main = Main()
