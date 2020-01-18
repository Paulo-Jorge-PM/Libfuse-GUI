#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading, os
import secrets
from flask import Blueprint, render_template, current_app, jsonify, json, Response, request, redirect, url_for

from core import libfuse, tools

#flaskRoutes = um Decorator da function routes do Flask started em gui.py
flaskRoutes = Blueprint('routes', __name__)

#===General config for templates without router
@flaskRoutes.context_processor
def globalContext():
    #Give flask app context to auth, for communication with libfuse
    if current_app.auth.flaskContext == None:
        current_app.auth.flaskContext = current_app
    if current_app.auth.user:
        user = current_app.auth.user
        username = current_app.auth.user.username
        userpath = current_app.auth.user.userPath
        verification = current_app.auth.verification
        email = current_app.auth.user.email
    else:
        username = ""
        userpath = ""
        verification = False
        email = ""
    loginStatus = current_app.auth.loginStatus
    return dict(username=username, loginStatus=loginStatus, MOUNTPOINT=current_app.configs[1], ROOTPATH = current_app.configs[2], userpath=userpath, verification=verification, email=email)

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
    path = "models/storage" + current_app.configs[1].split("/")[-1]
    #os.system('gnome-terminal --working-directory='+'"'+ current_app.configs[1]+'"')
    os.system('gnome-terminal --working-directory='+'"'+ path +'"')
    return Response("ok")

@flaskRoutes.route('/folder')
def folder():
    os.system('xdg-open ' + '"' + current_app.configs[1] + '"')
    return Response("ok")

@flaskRoutes.route('/start')
def start():
    #tools.checkDirs(current_app.configs[2], current_app.configs[1])

    userpath = current_app.auth.user.userPath
    libfuse = threading.Thread(target=fuseThread, args=(userpath, current_app.configs[1], current_app.auth))
    libfuse.daemon = True
    libfuse.start()
    return Response("Start ok")
    #libfuse = libfuse.main(root=current_app.configs[2],mountpoint=current_app.configs[1])

def fuseThread(r, m, auth):
    libfuse.main(root=r,mountpoint=m, auth=auth)

@flaskRoutes.route('/stop')
def stop():
    #import fuse
    #fuse.fuse_exit()
    os.system("fusermount -u " + '"' +  current_app.configs[1] + '"')
    return Response("Unmount ok")

#===Pages routes
@flaskRoutes.route('/')
def index():
    #if current_app.auth.user:
    try:
        userFile = "user" + str(current_app.auth.user.idUser) + ".txt"
        userFilePath = os.path.join(current_app.configs[2],userFile)
        logUser = tools.tail(userFilePath, n=20)
    except:
        logUser = ""
    #userpath = current_app.auth.user.userPath
    return render_template("index.html", logUser=logUser)

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

@flaskRoutes.route('/admin')
def admin():
    return render_template("admin.html")

@flaskRoutes.route('/logs')
def logs():
    try:
        userFilePath = os.path.join(current_app.configs[1],"log.txt")
        logUser = tools.tail(userFilePath, n=100)
    except:
        logUser = ""
    return render_template("logs.html", logUser=logUser)

@flaskRoutes.route('/logout')
def logout():
    current_app.auth.logout()
    return redirect( url_for('.index') )

@flaskRoutes.route('/sendcode')
def sendcode():
    code = secrets.token_urlsafe()
    m = "O seu código de validação para a App SSI é: " + code
    current_app.auth.verificationCode = code
    tools.sendEmail(message=m, to=current_app.auth.user.email)
    return Response("Email sent")

@flaskRoutes.route('/codeverification', methods=['GET', 'POST'])
def codeverification():
    if request.method == 'POST':
        if request.form:
            code = request.form["code"]
    if current_app.auth.verificationCode == code:
        current_app.auth.verification = True
        #message = "Código de validação correto! Opção open desbloqueada com sucesso! Pode voltar à página inicial e continuar a "
        return redirect( url_for('.refresh') )
    else:
        current_app.auth.verification = False
        message = "Código de validação errado! Por favor volte à página inicial e tente novamente."
        return render_template("message.html", message=message)

    #message = ""
    #code = "empty"
    #return render_template("verification.html")

@flaskRoutes.route('/resetcode')
def resetcode():
    current_app.auth.verification = False
    #return redirect( url_for('.refresh'), code=302 )
    return redirect( 'index' )



@flaskRoutes.route('/refresh')
def refresh():
    return redirect( url_for('.index') )