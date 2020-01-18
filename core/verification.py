#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask
from flask_mail import Mail

#pip install Flask-Mail

app = Flask(__name__)
mail = Mail(app)

@app.route("/mail")
def mail(email):
    msg = Message("SSI/MEI TP3: Code Confirmation",
                  sender="b4701@ilch.uminho.pt",
                  recipients=[email])
    msg.html = "<h1>Filesystem Manager:</h1><br><p>Please open this URL to confirm:</p>"
    mail.send(msg)
