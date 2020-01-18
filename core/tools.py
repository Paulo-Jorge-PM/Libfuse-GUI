#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, shutil
import smtplib, ssl
from email.mime.text import MIMEText
from collections import deque

def createDir(path, mode='0700'):
    #makedirs honors unmask, so in some systems permissions are ignored
    #So we first ignore unmask
    try:
        original_umask = os.umask(0)
        if not os.path.exists(path):
            #os.makedirs(path, int(mode))
            os.makedirs(path)
    except:
        print("Error - not possible to create directory")
    finally:
        os.umask(original_umask)


def removeMount(path):
    #delete 1st
    shutil.rmtree(path)

def createLog(path, line):
    f = open(path, "a")
    f.write(line)
    f.close()



#Read n lines from end of file
def tail(filename, n=10):
    with open(filename) as f:
        return deque(f, n)




def sendEmail(message="", to="paulo.jorge.pm@gmail.com"):
    """smtp_server = "mail.uminho.pt"
    port = 25
    username = "b4701"
    sender_email = "b4701@ilch.uminho.pt"
    password = "11J11YK5"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(username, password)
        server.sendmail(sender_email, to, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() """


    SERVER = "mail.uminho.pt"
    PORT = "25"
    USER = "b4701"
    PASS = "11J11YK5"
    FROM = "b4701@ilch.uminho.pt"
    TO = [to]
    SUBJECT = 'SSI CODE VALIDATE'

    # Create the email
    message = MIMEText(message)
    message['From'] = FROM
    message['To'] = ",".join(TO)
    message['Subject'] = SUBJECT

    # Sends an email
    email = smtplib.SMTP()
    email.connect(SERVER,PORT)
    email.starttls()
    email.login(USER,PASS)
    email.sendmail(FROM, TO, message.as_string())
    email.quit()
    #return redirect( url_for('sucess'))