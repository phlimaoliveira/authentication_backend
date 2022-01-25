import os
import re
from datetime import datetime, timedelta
from flask import Response, jsonify
from ORM.User import User
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash

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