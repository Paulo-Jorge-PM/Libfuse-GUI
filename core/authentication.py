#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random, datetime, os

from models import db
from core import client, admin, tools
from views import routes

class Auth:

    def __init__(self, configs=None, username=None, password=None, webviewContext=None, flaskContext=None):
        self.configs = configs
        self.webviewContext = webviewContext
        self.flaskContext = None

        self.db = db.Db()

        self.user = None
        self.loginStatus = False
        self.verificationCode = None
        self.verification = False

        #For terminal login with params withou GUI
        if username and password:
            self.login(username, password)

    def login(self, username, password):
        user = self.db.loginUser(username,password)
        if user:
            userPath = self.checkDir(user["id"], user["uid"])
            if user["userRole"] == "user":
                self.user = client.Client(user["id"], user["username"], user["email"], user["password"], user["uid"], user["userRole"], user["dateRegistration"], userPath)
            elif user["userRole"] == "admin":
                self.user = admin.Admin(user["id"], user["username"], user["email"], user["password"], user["uid"], user["userRole"], user["dateRegistration"], userPath)
            
            self.loginStatus = True
            return True
        else:
            self.user = None
            self.loginStatus = False
            return False

    def register(self, name, email, password, uid):
        dateReg = datetime.datetime.now()
        try:
            self.db.insertUser(username=name, email=email, password=password, uid=uid, dateRegistration=dateReg)
            
            return True
        except Exception as error:
            print(error)
            return False

    def checkDir(self, userid, uid):
        dirpath = os.path.join(self.configs[2], "userid"+str(userid))
        tools.createDir(dirpath)
        tools.dirCHOWN(dirpath, uid)
        return dirpath

    def logout(self):
        self.user = None
        self.loginStatus = False

    def log(self, message=None):
        from datetime import datetime
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        if self.verification == True:
            verification_code = "success"
        else:
            verification_code = "none"

        line = ">LOG: " + now + " | " + "Verification: " + verification_code + " | Log: " + message + os.linesep
        tools.createLog(path=os.path.join(self.configs[2],"log.txt"), line=line)
        user_file = "user" + str(self.user.idUser) + ".txt"
        tools.createLog(path=os.path.join(self.configs[2],user_file), line=line)
        print(line)

        #self.webviewContext.load_url('http://127.0.0.1:5000/')
        #with self.flaskContext.app_context():
        #    print(current_app.auth.user.username)



        """if self.verification == True:
            line = now + " | User: #" + user["id"] + " | Status: SUCCESS (VERIFIED) | Log: " + message
            tools.createLog(path=os.path.join(self.configs[2],"log.txt"), line=message)
            print(line)
            return True
        else:
            line = now + " | " + "Status: FAILED (NOT VERIFIED) | Log: " + message
            tools.createLog(path=os.path.join(self.configs[2],"log.txt"), line=message)
            print(line)
            return False"""

    def verification(self):

        return True

