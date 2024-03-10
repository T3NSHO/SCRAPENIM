from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from scrapping_fncts import check_creds, enim_login , get_grades
import os


app = Flask(__name__)

#import localvariables HHHHH knt mwlf ndirhom plaintext I was like naaah this time this is going to github XDD
secret_key = os.getenv('SECRET_KEY')
api_username = os.getenv('api_user')
api_password = os.getenv('api_password')
app.config["JWT_SECRET_KEY"] = secret_key
jwt = JWTManager(app)


print(api_password , api_username)
@app.route("/login" , methods=["POST"])
def login():
    print("request received")
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != api_username or password != api_password:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/verify_creds" , methods=["POST"])
def verify_creds():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    response , session = enim_login(username, password)
    data = check_creds(response,session)
    return data
    
    