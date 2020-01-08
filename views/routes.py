#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading, os
from flask import Blueprint, render_template, current_app, jsonify, json, Response, request, redirect, url_for

from core import libfuse, tools

#flaskRoutes = um Decorator da function routes do Flask started em gui.py
flaskRoutes = Blueprint('routes', __name__)

#===General config for templates without router
@flaskRoutes.context_processor
def globalContext():
    if current_app.auth.user:
        username = current_app.auth.user.username
    else:
        username = ""
    loginStatus = current_app.auth.loginStatus
    return dict(username=username, loginStatus=loginStatus, MOUNTPOINT=current_app.configs[1], ROOTPATH = current_app.configs[2])

#===Disable cache for all pages
@flaskRoutes.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


#===Ajax API Assíncrona
@flaskRoutes.route('/assets')
def checkCode():
    pass

@flaskRoutes.route('/terminal')
def terminal():
    #multi distro: xterm | gnome: gnome-terminal
    os.system('gnome-terminal --working-directory='+'"'+ current_app.configs[1]+'"')
    return Response("ok")

@flaskRoutes.route('/folder')
def folder():
    os.system('xdg-open ' + '"' + current_app.configs[1] + '"')
    return Response("ok")

@flaskRoutes.route('/start')
def start():
    tools.checkDirs(current_app.configs[2], current_app.configs[1])
    libfuse = threading.Thread(target=fuseThread, args=(current_app.configs[2], current_app.configs[1]))
    libfuse.daemon = True
    libfuse.start()
    return Response("ok")
    #libfuse = libfuse.main(root=current_app.configs[2],mountpoint=current_app.configs[1])

def fuseThread(r, m):
    libfuse.main(root=r,mountpoint=m)

@flaskRoutes.route('/stop')
def stop():
    #import fuse
    #fuse.fuse_exit()
    os.system("fusermount -u " + current_app.configs[1])
    return Response("ok")

#===Pages routes
@flaskRoutes.route('/')
def index():
    return render_template("index.html", data="")

@flaskRoutes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #To do: validation and sanitazion. Now it is only in front-end view very light
        if request.form:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            reg = current_app.auth.register(username,email,password)
            if reg == True:
                message="success"
            else:
                message="error"
        else:
            message="error"
        return render_template("register.html", status=message)
    else:
        return render_template("register.html", status="ask")

@flaskRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form:
            username = request.form["username"]
            password = request.form["password"]
            login = current_app.auth.login(username,password)
            if login == True:
                message="success"
            else:
                message="error"
    else:
        message="ask"
    return render_template("login.html", status=message)


@flaskRoutes.route('/logout')
def logout():
    current_app.auth.logout()
    return redirect( url_for('.index') )
