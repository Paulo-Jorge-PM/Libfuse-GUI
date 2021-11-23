#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
pydal : ORM / Database Abstraction Layer
"""

from pydal import DAL, Field

import os
current_dir = os.path.dirname(os.path.abspath(__file__))

class Db:

    def __init__(self):
        self.uri = 'sqlite://database.sqlite'
        self.folder = os.path.join(current_dir, "sqlite")

        self.db = None

    def connect(self):
        if not self.db:
            self.db = DAL(self.uri, folder=self.folder, pool_size=5, migrate_enabled=False, migrate=False, lazy_tables=True)
            #self.db = DAL(self.uri, folder=self.folder, pool_size=5, 
            #,migrate_enabled=False, migrate=False, lazy_tables=True
            self.tables()
            self.db._adapter.reconnect()#in some cases gives thread error without
        else:
            print("Nota: db already open, closing and restarting connection")
            #close in case a process forgot to close
            self.close()
            self.connect()

    def close(self):
        self.db.close()
        self.db = None

    def tables(self):
        self.tableUsers()


    def tableUsers(self):
        try:
            #Note: id is created automattically if omited
            self.db.define_table('users', 
                Field('username', type='string'), 
                Field('email', type='string'),
                Field('password', type='string'),
                Field('uid', type='string'),
                Field('userRole', type='string', defaul='user'),#user, admin
                Field('secureKey', type='string', default='0', writable=False, readable=False),#secet key token - should be used if in server side
                Field('dateRegistration', type='datetime', writable=False, readable=False)
                )
        except:
            print('models db.DB() tableUsers Error')

    def tableLogs(self):
        pass


    def insertUser(self, username, email, password, uid, dateRegistration):
        self.connect()
        import secrets#generate url safe token
        secureKey = secrets.token_urlsafe()
        self.db.users.insert(username=username, email=email, password=password, uid=uid, userRole="user", secureKey=secureKey, dateRegistration=dateRegistration)
        self.db.commit()
        self.db.close()

    def loginUser(self, username, password):
        self.connect()
        user = self.db( (self.db.users.username == username) & (self.db.users.password == password) ).select().first()
        self.db.close()
        #if no user, it will return user = None
        return user

    def getUsers(self):
        self.connect()
        users = self.db(self.db.users.id > 0 ).select()
        self.db.close()
        return users
