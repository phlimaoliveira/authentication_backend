import os
import re
from datetime import datetime, timedelta
from flask import Response, jsonify, render_template
from ORM.User import User
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail
from threading import Thread

class ManageUsers:
    #Register a New User
    def newUser(name, email, password):
        if (isValidEmail(email) == False):
            return Response("E-mail is not valid", status=400)
        else:
            user = User()
            user.name = name
            user.email = email
            user.password = generate_password_hash(password)
            user.save()

            return Response("User inserted with success", status=201)

    # Do Login on System
    def login(email, password):
        user = User.objects(email__exact=email).first()

        if user and check_password_hash(user.password, password):
            payload_data = {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
            }

            expires = timedelta(hours=24)
            token = create_access_token(identity=payload_data, expires_delta=expires)

            return { "access_token": token }, 202
        else:
            return Response("Invalid Credentials!", status=401)

    def forgotPassword(email):
        if(userExists(email) == False):
            return Response("Email not exists on database!", status=401)
        else:
            payload_data = {
                "reset_password": True,
                "email": email,
            }

            expires = timedelta(minutes=30)
            return create_access_token(identity=payload_data, expires_delta=expires)

    def sendMailForgotPassword(reset_token, email, app, mail):
        try:
            msg = Message()
            msg.subject = "VueJS Authentication Password Reset"
            msg.sender = os.getenv('MAIL_USERNAME')
            msg.recipients = email.split()
            msg.html = render_template('reset_email.html', reset_token=reset_token)
            Thread(target=send_email, args=(app, msg, mail)).start()

            return Response("Email sent to user recovery your password!", status=200)
        except:
            return Response("An error occurred! Please try again!", status=400)

    def updatePassword(email, new_password):
        try:
            user = User.objects(email__exact=email).first()
            user.password = generate_password_hash(new_password)
            user.save()

            return Response("Password updated!", status=200)
        except:
            return Response("An error occurred! Please try again!", status=400)


def send_email(app, msg, mail):
    with app.app_context():
        mail.send(msg)

#Checking if User Exists
def userExists(email):
    user = User.objects(email__exact=email).first()

    if(user): return True
    else: return False

# True is a valid email
def isValidEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (re.fullmatch(regex, email)): return True
    else: return False