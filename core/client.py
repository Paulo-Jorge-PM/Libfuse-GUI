#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core import user
from models import db

class Client(user.User):

    #def __init__(self, username, email, password, userRole):
    def __init__(self, idUser, username, email, password, userRole, dateRegistration, userPath):
        super().__init__(idUser, username, email, password, userRole, dateRegistration, userPath)
        self.userRole = "user"

    def logs(self):
        logs = db.Db().logs(self.idUser)
        return logs

    def checkAuth(self):
        pass
    
    def profile(self):
        pass

    def editProfile(self):
        pass
