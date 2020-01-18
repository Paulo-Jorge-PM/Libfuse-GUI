#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core import user
#from core import management

class Admin(user.User):

    def __init__(self):
        super().__init__()
        self.___action = None

    def checkAuth(self):
        pass
    
    def editProfile(self):
        pass

    def manage(self):
        pass
