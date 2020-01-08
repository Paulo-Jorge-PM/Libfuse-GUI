#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import webview
import sys
import threading

from flask import Flask
from views.routes import flaskRoutes
from core.libfuse import main

class Gui(Flask):
    def __init__(self, import_name=__name__, auth=None, configs=None):
        super(Gui, self).__init__(import_name=__name__, static_folder='static', template_folder='templates')

        self.configs = configs
        self.auth = auth
        
        #Start a Flask server in a thread
        self.server = threading.Thread(target=self.startServer)
        self.server.daemon = True
        self.server.start()

        #Start weview GUI
        self.webview = self.startWebview()


    def startServer(self):
        self.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0# disable caching so it refresh the view in each start
        self.configApp()
        self.register_blueprint(flaskRoutes)
        self.run(debug=False, threaded=False)

    def startWebview(self):
        webview.create_window("MEI", "http://127.0.0.1:5000/")
        webview.start()
        return webview

    #CONFIGURATIONS SAVE
    def configApp(self):
        self.config.update(
            GUI = self.configs[0],
            MOUNTPOINT = self.configs[1],
            ROOTPATH = self.configs[2]
        )