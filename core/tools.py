#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, shutil
import smtplib, ssl
from email.mime.text import MIMEText
from collections import deque

#mode='0700'
def createDir(path, mode='700'):
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


def dirCHOWN(path, uid):
    #os.setuid(int(uid))
    #shutil.chown(path, user=uid)
    os.chown(path, int(uid), int(uid))

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




def sendEmail(message, to):
    SERVER = "mail.uminho.pt"
    PORT = "25"
    USER = "b4701"
    PASS = "11J11YK5"
    FROM = "b4701@elach.uminho.pt"
    TO = [to]
    SUBJECT = 'SSI CODE VALIDATE'

    # email
    message = MIMEText(message)
    message['From'] = FROM
    message['To'] = ",".join(TO)
    message['Subject'] = SUBJECT

    # send email
    email = smtplib.SMTP(SERVER)
    email.connect(SERVER,PORT)
    email.starttls()
    email.login(USER,PASS)
    email.sendmail(FROM, TO, message.as_string())
    email.quit()
    print("E-mail enviado para: " + to)
