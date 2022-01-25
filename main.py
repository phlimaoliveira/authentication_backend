import os
from datetime import datetime, timezone
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, unset_jwt_cookies, set_access_cookies, get_jwt
from flask_mongoengine import MongoEngine
from ORM.TokenBlocklist import TokenBlocklist
from core.ManageTokenBlocklist import ManageTokenBlocklist

from core.ManageUsers import ManageUsers, userExists

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

load_dotenv()
CORS(app)

app.config['MONGODB_SETTINGS'] = { "db": "auth_vuejs" }
db = MongoEngine(app)

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    print(jti)
    token = TokenBlocklist.objects(jti__exact=jti).first()
    return token is not None

# Endpoint for revoking the current users access token. Saved the unique
# identifier (jti) for the JWT into our database.
@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    ManageTokenBlocklist.new(jti, now)
    return jsonify(msg="JWT revoked")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    return ManageUsers.login(email, password)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = str(data.get('password'))

    return ManageUsers.newUser(name, email, password)

@app.route('/verify_email_user/<email>', methods=['GET'])
def verifyEmailUserExists(email):
    return Response(str(userExists(email)), status=200)

@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    return 'Authenticated Sucess'

if __name__ == '__main__':
    app.run(debug=True)
