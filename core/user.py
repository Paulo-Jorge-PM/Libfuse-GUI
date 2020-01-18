#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
from core import authentication

class User(metaclass = ABCMeta):

    @abstractmethod
    def __init__(self, idUser, username, email, password, uid, userRole, dateRegistration, userPath):
        self.idUser = idUser
        self.username = username
        self.email = email
        self.password = password
        self.uid = uid
        self.userRole = userRole
        self.dateRegistration = dateRegistration
        self.userPath = userPath
        #self.secureKey = None

    #@classmethod
    @abstractmethod
    def profile(self):
        pass

    @abstractmethod
    def editProfile(self):
        pass

    @abstractmethod
    def checkAuth(self):
        pass
