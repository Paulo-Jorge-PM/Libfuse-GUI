#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
import datetime

from models import db


class Auth:

    def __init__(self, configs):
        self.configs = configs

        self.db = db.Db()

        self.user = None
        self.loginStatus = False

    def login(self, username, password):
        user = self.db.loginUser(username,password)
        if user:
            if user["userRole"] == "user":
                self.user = investor.Investor(user["id"], user["username"], user["email"], user["password"], user["balance"], user["userRole"], user["dateRegistration"])
            elif user["userRole"] == "admin":
                self.user = admin.Admin(user["id"], user["username"], user["email"], user["password"], user["balance"], user["userRole"], user["dateRegistration"])

            self.loginStatus = True
            return True
        else:
            self.user = None
            self.loginStatus = False
            return False

    def register(self, name, email, password):
        dateReg = datetime.datetime.now()
        try:
            self.db.insertUser(username=name, email=email, password=password, dateRegistration=dateReg)
            return True
        except Exception as error:
            print(error)
            return False

    def logout(self):
        self.user = None
        self.loginStatus = False
